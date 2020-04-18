import unittest
import csv
from csv import DictReader
from network.securitygroup.securityrule import SecurityRule
import json
from collections import defaultdict
from collections import OrderedDict
from parser.csvparser import CSVParser
from network.securitygroup.nsglist import NSGList
import io

class Test_CSV(unittest.TestCase):
    CLI_PARAMS_DICT = [{'name':'rulename','cmd':'--name'}, {'name':'nsgname', 'cmd':'--nsg-name'}, {'name':'priority', 'cmd':'--priority'}, 
    {'name':'resourceGroup', 'cmd':'--resource-group'}, {'name':'access', 'cmd':'--access'}, {'name':'description', 'cmd':'--description'}, 
    {'name':'destinationAddressPrefixes', 'cmd':'--destination-address-prefixes'}, 
    {'name':'destinationAsgs', 'cmd':'--destination-asgs'},{'name':'destinationPortRanges', 'cmd':'--destination-port-ranges'}, 
    {'name':'direction', 'cmd':'--direction'}, {'name':'protocol', 'cmd':'--protocol'}, 
    {'name':'sourceAddressPrefixes', 'cmd':'--source-address-prefixes'}, {'name':'sourceAsgs','cmd':'--source-asgs'}, 
    {'name':'sourcePortRanges', 'cmd':'--source-port-ranges'}]


    def switch_values(arg:dict, key:str):
        switcher = {
        "rulename": arg["rulename"],
        "nsgname": arg["nsgname"],
        "priority": arg["priority"],
        "resourceGroup": arg["resourceGroup"],
        "access": arg["access"],
        "description": arg["description"],
        "destinationAsgs": arg["destinationAsgs"],
        "destinationPortRanges": arg["destinationPortRanges"],
        "sourceAddressPrefixes": arg["sourceAddressPrefixes"],
        "sourceAsgs": arg["sourceAsgs"],
        "sourcePortRanges": arg["sourcePortRanges"]
        }
        return switcher.get(arg, "Invalid month")

    def test_dictreader(self):
        cmd:str = ""
        nsglist:NSGList = NSGList()
        names=[]
        commands=[]
        sample = """resourceGroup,location,nsgname,rulename,description,protocol,sourcePortRange,destinationPortRange,sourceAddressPrefix,destinationAddressPrefix,access,priority,direction,sourcePortRanges,destinationPortRanges,sourceAddressPrefixes,destinationAddressPrefixes
dev,eastus,linux1,Port_3389,description,TCP,*,3389,*,*,Allow,100,Inbound,[],[],[],[]"""

        nsglist = CSVParser("x")._doParseToNSGList(csv.DictReader(io.StringIO(sample)))    

        for nsgName, rules in nsglist.nsgDict.items():
            rule:SecurityRule
            for rule in rules:
                for gen in (item for item in self.CLI_PARAMS_DICT):
                    names.append(gen["name"])
                    commands.append(gen["cmd"])
                    rule.getAttributeValueByName(gen["name"])
        
        for nsgName, rules in nsglist.nsgDict.items():
            rule:SecurityRule
            for rule in rules:
                for gen in (item for item in self.CLI_PARAMS_DICT):
                    print(f"Testing: {gen['name']}, {gen['cmd']}")
                    self.assertIn(gen["name"], names)
                    self.assertIn(gen["cmd"], commands)
                    rule.getAttributeValueByName(gen["name"])

        