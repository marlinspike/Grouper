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

    def test_dictreader(self):
        nsglist = NSGList()
        sample = """resourceGroup,location,nsgname,rulename,description,protocol,sourcePortRange,destinationPortRange,sourceAddressPrefix,destinationAddressPrefix,access,priority,direction,sourcePortRanges,destinationPortRanges,sourceAddressPrefixes,destinationAddressPrefixes
dev,eastus,linux1,Port_3389,description,TCP,*,3389,*,*,Allow,100,Inbound,[],[],[],[]"""

        nsglist = CSVParser("x")._doParseToNSGList(csv.DictReader(io.StringIO(sample)))
        self.assertTrue("linux1" in nsglist.getAllNSGs())
        rule:SecurityRule = nsglist.nsgDict["linux1"]
        self.assertEqual("eastus",rule[0].location)
        self.assertEqual("Port_3389",rule[0].rulename)
        self.assertEqual("eastus",rule[0].location)
        self.assertEqual("description",rule[0].description)
        self.assertEqual("TCP",rule[0].protocol)
        self.assertEqual("*",rule[0].sourcePortRange)
        self.assertEqual("3389",rule[0].destinationPortRange)
        self.assertEqual("*",rule[0].sourceAddressPrefix)
        self.assertEqual("*",rule[0].sourceAddressPrefix)
        self.assertEqual("Allow",rule[0].access)
        self.assertEqual("100",rule[0].priority)
        self.assertEqual("Inbound",rule[0].direction)
        self.assertEqual('[]',rule[0].sourcePortRanges)
        self.assertEqual("[]",rule[0].destinationPortRanges)
        self.assertEqual("[]",rule[0].sourceAddressPrefixes)
        self.assertEqual("[]",rule[0].destinationAddressPrefixes)




        