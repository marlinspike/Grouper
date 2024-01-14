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


class NSGList:
    """
    Represents a list of Network Security Groups (NSGs), each of which has zero or many SecurityRules.

    This class contains methods to add SecurityRule objects to the NSG list, get all NSGs in the list, 
    and convert the NSG list to a string for debugging purposes.

    Attributes:
        nsgDict (defaultdict): A dictionary where the keys are NSG names and the values are lists of SecurityRule objects.
        nsg_rg_lookup (dict): A dictionary that maps NSG names to their corresponding resource groups.
        separator (str): The character used to separate elements when converting the NSG list to a string.
    """
    def __init__(self):
        self.nsgDict = defaultdict(list)
        self.nsg_rg_lookup = {} #Maps NSG to a Resource Group
        self.separator = ","


    def addToDict(self, securityRule:SecurityRule):
        """
        Adds a SecurityRule object to the NSG list.

        This method adds the provided SecurityRule object to the NSG list. The NSG name from the SecurityRule object 
        is used as the key in the NSG dictionary, and the SecurityRule object itself is appended to the list of 
        SecurityRule objects associated with that NSG.

        Args:
            securityRule (SecurityRule): The SecurityRule object to be added to the NSG list.
    """
        if securityRule is not None:
            self.nsgDict[securityRule.nsgname].append(securityRule)



    def getAllNSGs(self) -> list:
        """
        Adds a SecurityRule object to the NSG list.

        This method adds the provided SecurityRule object to the NSG list. The NSG name from the SecurityRule object 
        is used as the key in the NSG dictionary, and the SecurityRule object itself is appended to the list of 
        SecurityRule objects associated with that NSG.

        Args:
            securityRule (SecurityRule): The SecurityRule object to be added to the NSG list.
        """
        lst_NSG = []
        for item in self.nsgDict.keys():
            lst_NSG.append(item)
        
        return lst_NSG


    def __str__(self) -> str:
        """
        Returns a string representation of the NSG list.

        This method returns a string representation of the NSG dictionary, which contains NSG names as keys and lists 
        of SecurityRule objects as values.

        Returns:
            str: A string representation of the NSG list.
        """
        return self.nsgDict.__str__()
    

  
    def getDebug(self) -> str:
        """
        Returns a string representation of the NSG list for debugging purposes.

        This method iterates over each NSG in the NSG dictionary, and for each NSG, it iterates over its associated 
        SecurityRule objects. It adds the string representation of each SecurityRule object to a string, separated by 
        newlines. It then returns this string.

        Returns:
            str: A string representation of the NSG list for debugging purposes.
        """
        s = ""
        for key, val in self.nsgDict.items():
            print(key)
            for l in val:
                s += l.__str__() + "\n"
        return s
