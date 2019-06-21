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

class CLIWriter:
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
    

    ###
    # Returns attribute value
    def getAttrLength(self, attr) -> int:
        return len(attr) if attr != "[]" else 0



    ###
    # Writes a CLI Script out, with each NSG mapped to an individual file  
    def doWrite_CLIScript(self, nsgList:NSGList, path:str) -> bool:
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
