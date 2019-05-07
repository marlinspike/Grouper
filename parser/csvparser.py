import csv
from network.securitygroup.securityrule import SecurityRule
from network.securitygroup.nsglist import NSGList

class CSVParser:

    def __init__(self, filename):
        self.filename = filename
    
    ###
    # Parse the CSV File to populate an NSGList with a SecurityRule object for each row
    # Returns: NSGList - List of NSG objects with their corresponding SecurityRule objects
    def doCSVParse(self) -> NSGList:
        nsglist = NSGList()
        with open(self.filename) as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                rule = SecurityRule().createFromOrderedDict(row)
                nsglist.addToDict(rule)
                nsglist.nsg_rg_lookup[row["nsgname"]] = row["resource_group"]

        return nsglist