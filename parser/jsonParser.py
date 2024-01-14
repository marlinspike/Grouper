import subprocess
import json
import yaml
from network.securitygroup.securityrule import SecurityRule
from collections import defaultdict
from network.securitygroup.nsglist import NSGList
import logging
from logger_config import setup_logger

setup_logger()

CMD_GET_NSG_LIST = "az network nsg list -o json"
CMD_GET_AZ_ACCOUNT = "az account show -o json"


class JSONParser:
    """
    A class used to parse JSON files.

    This class contains methods to read and parse JSON files. It is designed to handle JSON files 
    that contain information about Network Security Groups (NSGs) and their rules.

    Attributes:
        filename (str): The name of the JSON file to be parsed.
    """
    def __init__(self):
        self.nsgDict = defaultdict(list)
        self.nsg_rg_lookup = {} #Maps NSG to a Resource Group
        self.separator = ","

    def parseJson(self) -> NSGList:
        """
        Parses a JSON document and returns a list of NSG rule mappings.

        This method runs a command to get the NSG list from Azure via the CLI, and then parses the resulting JSON document. 
        It iterates over each NSG in the document, and for each NSG, it iterates over its security rules. For each rule, 
        it creates a new SecurityRule object and adds it to the NSGList. It also updates the NSG resource group lookup 
        dictionary with the NSG name and its corresponding resource group.

        Returns:
            NSGList: A list of NSGs parsed from the JSON document.
        """
        doc = {}
        try:
            doc = json.loads(subprocess.run([CMD_GET_NSG_LIST], check=False, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8'))
        except:
            print("An error occurred accessing Azure via the CLI. Please verify your CLI installation, or login to Azure via 'az login' before continuing.")
            logging.error("An error occurred accessing Azure via the CLI. Please verify your CLI installation, or login to Azure via 'az login' before continuing.")
            
        nsgCount = len(doc)
        ruleCount:int
        nsgIdx:int 
        ruleIdx:int
        nsgName: str
        nsglist = NSGList()
        rule:SecurityRule

        # Loop through each Network Security Group (NSG) in the document
        for nsgIdx in range(nsgCount):
            # Get the number of security rules in the current NSG
            ruleCount = len(doc[nsgIdx]["securityRules"])
            # Get the name of the current NSG
            nsgName = doc[nsgIdx]["name"]
            # Loop through each security rule in the current NSG
            for ruleIdx in range(ruleCount):
                # Get the current security rule
                row = doc[nsgIdx]["securityRules"][ruleIdx]
                # Add the location of the current NSG to the security rule
                row["location"] = doc[nsgIdx]["location"]
                # Add the name of the current NSG to the security rule
                row["nsgname"] = nsgName
                # Add the name of the security rule to the security rule
                row["rulename"] = row["name"]
                # Add the current NSG to the NSG lookup dictionary in the NSG list
                nsglist.nsg_rg_lookup[row["nsgname"]] = nsgName
                row["description"] = ""
                row["destinationPortRange"] = ""
                row["sourceAddressPrefix"] = ""
                # Add the current security rule to the NSG list
                nsglist.addToDict(SecurityRule().createFromOrderedDict(row))

        logging.info(f"Successfully parsed JSON document. NSG count: {nsgCount}")

        return nsglist

    def parseAzureAccountJson(self) -> {}:
        """
        Returns current Azure account information.

        This method runs a command to get the current Azure account information via the CLI, and then parses the 
        resulting JSON document. If an error occurs during this process, it prints an error message and returns an 
        empty dictionary.

        Returns:
            Dict: A dictionary containing the current Azure account information, or an empty dictionary if an error occurred.
        """
        azAct = {}
        try:
            azAct = json.loads(subprocess.run([CMD_GET_AZ_ACCOUNT], check=False, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8'))
        except:
            print("An error occurred accessing Azure via the CLI. Please verify your CLI installation, or login to Azure via 'az login' before continuing.")
            logging.error("An error occurred accessing Azure via the CLI. Please verify your CLI installation, or login to Azure via 'az login' before continuing.")
        return azAct
