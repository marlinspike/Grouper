'''
    File name: cliwriter.py
    Author/Maintainer: Reuben Cleetus
    email:reuben@cleet.us
    Copyright: 2019
    License: GPL 3.0
    Python Version:3.7
'''
from network.securitygroup.nsglist import NSGList
from network.securitygroup.securityrule import SecurityRule
from pathlib import Path
from collections import defaultdict
import os
import logging
from logger_config import setup_logger

setup_logger()

class CLIWriter:
    """
    A class used to generate Azure CLI scripts for creating network security group (NSG) rules.

    This class contains methods to generate Azure CLI scripts based on the provided NSG rules. 
    It uses a predefined dictionary to map parameter names to their corresponding Azure CLI options. 
    The scripts are written to a specified file.

    Attributes:
        filename (str): The name of the file to write the CLI scripts to.
    """
    CLI_PARAMS_DICT = [{'name':'rulename','cmd':'--name'}, {'name':'nsgname', 'cmd':'--nsg-name'}, {'name':'priority', 'cmd':'--priority'}, 
    {'name':'resourceGroup', 'cmd':'--resource-group'}, {'name':'access', 'cmd':'--access'}, {'name':'description', 'cmd':'--description'}, 
    {'name':'destinationAddressPrefixes', 'cmd':'--destination-address-prefixes'}, 
    {'name':'destinationAsgs', 'cmd':'--destination-asgs'},{'name':'destinationPortRanges', 'cmd':'--destination-port-ranges'}, 
    {'name':'direction', 'cmd':'--direction'}, {'name':'protocol', 'cmd':'--protocol'}, 
    {'name':'sourceAddressPrefixes', 'cmd':'--source-address-prefixes'}, {'name':'sourceAsgs','cmd':'--source-asgs'}, 
    {'name':'sourcePortRanges', 'cmd':'--source-port-ranges'}]
    CLI_SCRIPT = "az network nsg rule create "

    def __init__(self, filename):
        self.filename = filename
    

    def getAttrLength(self, attr) -> int:
        """
        Returns the length of the attribute.

        This method returns the length of the provided attribute. If the attribute is an empty list (represented as "[]"), 
        it returns 0.

        Args:
            attr (str): The attribute whose length is to be determined.

        Returns:
            int: The length of the attribute, or 0 if the attribute is an empty list.
        """
        return len(attr) if attr != "[]" else 0



    def doWrite_CLIScript(self, nsgList:NSGList, path:str) -> bool:
        """
        Writes the Azure CLI scripts to a file.

        This method generates Azure CLI scripts for each NSG and its rules in the provided NSG list. 
        It writes these scripts to a file in the specified path. If the output directory does not exist, 
        it is created.

        Args:
            nsgList (NSGList): A list of NSGs, each with its associated rules.
            path (str): The path where the CLI script file should be written.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        file_dict = {}
        script = self.CLI_SCRIPT
        isDone = True

        try:
            file_dir = os.path.join(path,"output")
            cli_file = os.path.join(path, "output", self.filename)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
                
            with open(cli_file, 'w') as cFile:
                for nsgName, rules in nsgList.items():
                    cFile.write(f"# {nsgName} \n")
                    rule:SecurityRule
                    for rule in rules:
                        cmd:str = ""
                        for gen in (item for item in self.CLI_PARAMS_DICT):
                            ruleValue = rule.getAttributeValueByName(gen["name"])
                            cmd = cmd + f" {gen['cmd']} {ruleValue} " if self.getAttrLength(ruleValue) > 0 else cmd
                        cFile.write(f"{self.CLI_SCRIPT + cmd} \n\n")
                    cFile.write("\n\n")
        except:
            isDone = False
        return isDone    
