from network.securitygroup.securityrule import SecurityRule
from collections import defaultdict

###
#Represents a list of NSGs, each of which has zero or many SecurityRules
class NSGList:
    def __init__(self):
        self.nsgDict = defaultdict(list)
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

     # ToString for this object
    def __str__(self) -> str:
        return self.nsgDict.__str__()
    

    ###
    #Prints out the NSGList for debug
    def printDebug(self):
        for key, val in self.nsgDict.items():
            print(key)
            for l in val:
                print(l)
