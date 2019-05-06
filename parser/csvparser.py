import csv
from network.securitygroup.securityrule import SecurityRule
from network.securitygroup.nsglist import NSGList

class CSVParser:

    def __init__(self, filename):
        self.filename = filename
    
    ###
    # Parse the CSV File to populate a SecurityRule object for each row
    def doCSVParse(self) -> NSGList:
        nsglist = NSGList()
        with open(self.filename) as csvFile:
            reader = csv.DictReader(csvFile)
            rule = SecurityRule()
            for row in reader:
                rule = rule.createFromOrderedDict(row)
                nsglist.addToDict(rule)
                #print(rule)
        
        return nsglist

    