import subprocess
import json
import yaml
from network.securitygroup.securityrule import SecurityRule
from collections import defaultdict
from network.securitygroup.nsglist import NSGList

CMD_GET_NSG_LIST = "az network nsg list -o json"
CMD_GET_AZ_ACCOUNT = "az account show -o json"


class JSONParser:
    def __init__(self):
        self.nsgDict = defaultdict(list)
        self.nsg_rg_lookup = {} #Maps NSG to a Resource Group
        self.separator = ","

    ###
    # Parses a Json doc and returns a Dict of NSG rule mappings
    def parseJson(self) -> NSGList:
        doc = {}
        try:
            doc = json.loads(subprocess.run([CMD_GET_NSG_LIST], check=False, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8'))
        except:
            print("An error occurred accessing Azure via the CLI. Please verify your CLI installation, or login to Azure via 'az login' before continuing.")
            
        nsgCount = len(doc)
        ruleCount:int
        nsgIdx:int 
        ruleIdx:int
        nsgName: str
        nsglist = NSGList()
        rule:SecurityRule

        for nsgIdx in range(nsgCount):
            ruleCount = len(doc[nsgIdx]["securityRules"])
            nsgName = doc[nsgIdx]["name"]
            for ruleIdx in range(ruleCount):
                row = doc[nsgIdx]["securityRules"][ruleIdx]
                row["location"] = doc[nsgIdx]["location"]
                row["nsgname"] = nsgName
                row["rulename"] = row["name"]
                nsglist.nsg_rg_lookup[row["nsgname"]] = nsgName
                nsglist.addToDict(SecurityRule().createFromOrderedDict(row))


        return nsglist

    ###
    # Returns current account information
    def parseAzureAccountJson(self) -> {}:
        azAct = {}
        try:
            azAct = json.loads(subprocess.run([CMD_GET_AZ_ACCOUNT], check=False, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8'))
        except:
            print("An error occurred accessing Azure via the CLI. Please verify your CLI installation, or login to Azure via 'az login' before continuing.")
        return azAct
