import subprocess
import json
import yaml
from network.securitygroup.securityrule import SecurityRule
from collections import defaultdict
from network.securitygroup.nsglist import NSGList

CMD_GET_NSG_LIST = "az network nsg list -o json"


class JSONParser:
    def __init__(self):
        self.nsgDict = defaultdict(list)
        self.nsg_rg_lookup = {} #Maps NSG to a Resource Group
        self.separator = ","

    ###
    # Parses a Json doc and returns a Dict of NSG rule mappings
    def parseJson(self) -> NSGList:
        doc = json.loads(subprocess.run([CMD_GET_NSG_LIST], check=False, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8'))

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
                rule = SecurityRule().createFromOrderedDict(row)
                nsglist.nsg_rg_lookup[row["nsgname"]] = nsgName
                nsglist.addToDict(rule)


        return nsglist