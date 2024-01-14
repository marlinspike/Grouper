'''
    File name: securityrule.py
    Author/Maintainer: Reuben Cleetus
    email:reuben@cleet.us
    Copyright: 2019
    License: GPL 3.0
    Date last modified: 5/8/2019
    Python Version:3.7
'''
from collections import OrderedDict
import copy
import json
import logging

class SecurityRule:
    def __init__(self):
        self.resourceGroup = ""
        self.location = ""
        self.nsgname = ""
        self.rulename = ""
        self.description = ""
        self.protocol = ""
        self.access = ""
        self.priority = ""
        self.direction = ""
        self.sourcePortRange = ""
        self.sourceAddressPrefix = ""
        self.destinationAddressPrefix = ""
        self.destinationPortRange = ""
        self.sourcePortRanges = []
        self.destinationPortRanges = []
        self.sourceAddressPrefixes = []
        self.destinationAddressPrefixes = []

        
        ###
        # Populates attributes in the current object, given another SecurityRule object
    def populateAttributes(self, obj:'SecurityRule'):
        self.resourceGroup = getattr(obj,"resourceGroup") if hasattr(obj, "resourceGroup") else ""
        self.location = getattr(obj,"location") if hasattr(obj, "location") else ""
        self.nsgname = getattr(obj, "nsgname") if hasattr(obj, "nsgname") else ""
        self.rulename = getattr(obj, "rulename") if hasattr(obj, "rulename") else ""
        self.description = getattr(obj, "description") if hasattr(obj, "description") else ""
        self.protocol = getattr(obj, "protocol") if hasattr(obj, "protocol") else ""
        self.sourcePortRange = getattr(obj, "sourcePortRange") if hasattr(obj, "sourcePortRange") else ""
        self.destinationPortRange = getattr(obj, "destinationPortRange") if hasattr(obj, "destinationPortRange") else ""
        self.sourcePortRanges = getattr(obj, "sourcePortRanges") if hasattr(obj, "sourcePortRanges") else ""
        self.destinationPortRanges = getattr(obj, "destinationPortRanges") if hasattr(obj, "destinationPortRanges") else ""
        self.sourceAddressPrefix = getattr(obj, "sourceAddressPrefix") if hasattr(obj, "sourceAddressPrefix") else ""
        self.destinationAddressPrefix = getattr(obj, "destinationAddressPrefix") if hasattr(obj, "destinationAddressPrefix") else ""
        self.sourceAddressPrefixes = getattr(obj, "sourceAddressPrefixes") if hasattr(obj, "sourceAddressPrefixes") else ""
        self.destinationAddressPrefixes = getattr(obj, "destinationAddressPrefixes") if hasattr(obj, "destinationAddressPrefixes") else ""
        self.access = getattr(obj, "access") if hasattr(obj, "access") else ""
        self.priority = getattr(obj, "priority") if hasattr(obj, "priority") else ""
        self.direction = getattr(obj, "direction") if hasattr(obj, "direction") else ""


    ###
    # Returns an AttrValDict
    def toDict(self) -> {}:
        return self._get_attribute_value_dictionary()

    ###
    # Returns an AttrValDict as OrderedDict
    def toOrderedDict(self) -> OrderedDict:
        oDict:OrderedDict = {k:v for (k,v) in self._get_attribute_value_dictionary().items()}
        return oDict

    #Create an instance of this class given a dictionary of attribute/value pairs
    def createFromDict(self, **kwargs) -> 'SecurityRule':
        lst_attributes = self._get_attribute_list()
        #self.description, self.protocol = [kwargs.get(k) for k in lst_attributes]
        for attribute in lst_attributes:
            self.__setattr__(attribute,kwargs.get(attribute))

        return self.createFromDeepCopy(self)
        #return SecurityRule(self.location, self.nsgname, self.rulename, self.description, self.protocol, self.sourcePortRange, self.destinationPortRange,
            #self.sourceAddressPrefix, self.destinationAddressPrefix, self.access, self.priority, self.direction)

    ###
    # Create an instance of this class given an OrderedDict object
    # Returns: SecurityRule based on the OrderedDict passed
    def createFromOrderedDict(self, OrderedDict) -> 'SecurityRule':
        lst_attributes = self._get_attribute_list()
        #self.description, self.protocol = [kwargs.get(k) for k in lst_attributes]
        for attribute in lst_attributes:
            self.__setattr__(attribute, OrderedDict[attribute])
        
        return self.createFromDeepCopy(self)



    ###
    # Create an instance of this class given an JSON object containing the necessary params
    # Returns: SecurityRule based on the JSON Object passed
    def createFromJson(self, JsonRule) -> 'SecurityRule':
        JsonDoc = json.loads(JsonRule)
        lst_attributes = self._get_attribute_list()
        #self.description, self.protocol = [kwargs.get(k) for k in lst_attributes]
        for attribute in lst_attributes:
            self.__setattr__(attribute, JsonDoc[attribute])
        
        return self.createFromDeepCopy(self)
    
    ###
    # Creates and returns a DeepCopy() SecurityRule object based on the one passed
    # Returns: SecurityRule based on the SecurityRule object passed
    @classmethod
    def createFromDeepCopy(self, obj:'SecurityRule') -> 'SecurityRule':
        rule = SecurityRule()
        
        rule.populateAttributes(obj)
        return rule



    ###
    # ToString for this object
    # Returns string representation of this object
    def __str__(self) -> str:
        val_dict = self._get_attribute_value_dictionary()
        lst = []

        for key, val in val_dict.items():
            lst.append(val)
        return ','.join(lst)
    
    ###
    # Gets list containing all the attributes of this class
    # Returns list of attributes of this object
    ###
    def _get_attribute_list(self) -> list:
        self_vars = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self,a))]
        return self_vars

    ###
    # Gets a dictionary with attribute name and value
    # Returns dict
    ###
    def _get_attribute_value_dictionary(self) -> dict:
        #s = locals()["self"]
        var_val = {}
        for attribute in self._get_attribute_list():
            var_val[attribute] = self.__getattribute__(attribute)
        return var_val

    
    def getAttributeValueByName(self, attr):
        dict = self._get_attribute_value_dictionary()
        val = dict[attr] if attr in dict else ""
        return val