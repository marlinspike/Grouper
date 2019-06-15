'''
    File name: csvparser.py
    Author/Maintainer: Reuben Cleetus
    email:reuben@cleet.us
    Copyright: 2019
    License: GPL 3.0
    Date last modified: 5/8/2019
    Python Version:3.7
'''
import csv
from network.securitygroup.securityrule import SecurityRule
from network.securitygroup.nsglist import NSGList
from collections import OrderedDict
from prefs.prefs import Preferences
import os

class CSVParser:

    def __init__(self, filename):
        self.filename = filename
        self.prefs = Preferences()
    
    ###
    # Parse the CSV File to populate an NSGList with a SecurityRule object for each row
    # Returns: NSGList - List of NSG objects with their corresponding SecurityRule objects
    def doCSVParse(self) -> NSGList:
        nsglist = NSGList()
        with open(self.filename) as csvFile:
            reader = csv.DictReader(csvFile)
            
            for row in reader:
                #Only add a rule if its priority is not in the Ignore List
                if (not row["priority"] in self.prefs.lst_ignore_priority):
                    rule = SecurityRule().createFromOrderedDict(row)
                    nsglist.addToDict(rule)
                    nsglist.nsg_rg_lookup[row["nsgname"]] = row["resourceGroup"]

        return nsglist

    ###
    # Reorders a dict of SecurityRule based on prefs
    def reorderDict(self, dict) -> OrderedDict:
        preferredOrder = Preferences().load_prefs("preferred_order").split(",")
        oDict = OrderedDict([item, ''] for item in preferredOrder) 

        for item in preferredOrder:
            oDict[item] = dict.get(item)

        return oDict


    ###
    # Writes a Grouper CSV File from an NSG List
    def writeCSVFromNSGList(self, nsgList:NSGList, path:str) -> bool:
        os_path = os.path.abspath(os.path.dirname(__file__))
        grouper_file = os.path.join(path, self.filename)

        with open(grouper_file, 'w') as gFile:
            lstAttrs = SecurityRule()._get_attribute_list()
            lstAttrs.append("resource_group")
            gWriter = csv.DictWriter(gFile, fieldnames = lstAttrs)
            gWriter.writeheader()

            for nsgName in nsgList.nsgDict:
                for rule in nsgList.nsgDict[nsgName]:
                    dict = self.reorderDict(rule.toDict())
                    gWriter.writerow(dict)
    


