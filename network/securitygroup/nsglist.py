'''
    File name: app.py
    Author/Maintainer: Reuben Cleetus
    email:reuben@cleet.us
    Copyright: 2019
    License: GPL 3.0
    Date last modified: 5/8/2019
    Python Version:3.7
'''
from network.securitygroup.securityrule import SecurityRule
from collections import defaultdict
__author__ = "Reuben Cleetus"
__copyright__ = "Copyright 2019"
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Reuben Cleetus"
__email__ = "reuben@cleet.us"
__status__ = "Production"

###
#Represents a list of NSGs, each of which has zero or many SecurityRules
class NSGList:
    def __init__(self):
        self.nsgDict = defaultdict(list)
        self.nsg_rg_lookup = {} #Maps NSG to a Resource Group
        self.separator = ","

    ###
    # Adds a SecurityRule object to the defaultdict collection
    def addToDict(self, securityRule:SecurityRule):
        if securityRule is not None:
            self.nsgDict[securityRule.nsgname].append(securityRule)


    ###
    # Returns a list of all NSGs that are tracked in the nsgDict collection
    def getAllNSGs(self) -> list:
        lst_NSG = []
        for item in self.nsgDict.keys():
            lst_NSG.append(item)
        
        return lst_NSG

    ###
    # ToString for this object
    # Returns str
    def __str__(self) -> str:
        return self.nsgDict.__str__()
    

    ###
    # Gets the NSGList for debug
    # Returns str
    def getDebug(self) -> str:
        s = ""
        for key, val in self.nsgDict.items():
            print(key)
            for l in val:
                s += l.__str__() + "\n"
        return s
