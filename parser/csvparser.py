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
from prefs.prefs import Preferences

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
                    nsglist.nsg_rg_lookup[row["nsgname"]] = row["resource_group"]

        return nsglist