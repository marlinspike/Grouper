from collections import OrderedDict

class SecurityRule:
    #location,nsgname,rulename,description,protocol,sourcePortRange,destinationPortRange,sourceAddressPrefix,destinationAddressPrefix,access,priority,direction,sourcePortRanges,destinationPortRanges,sourceAddressPrefixes,destinationAddressPrefixes
    def __init__(self):
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
    
    def populateAttributes(self, location, nsgname, rulename, description, protocol, sourcePortRange, destinationPortRange, sourcePortRanges, destinationPortRanges, 
    sourceAddressPrefix, sourceAddressPrefixes, destinationAddressPrefix, destinationAddressPrefixes, access, priority, direction):
        self.location = location
        self.nsgname = nsgname
        self.rulename = rulename
        self.description = description
        self.protocol = protocol
        self.sourcePortRange = sourcePortRange
        self.destinationPortRange = destinationPortRange
        self.sourcePortRanges = sourcePortRanges
        self.destinationPortRanges = destinationPortRanges
        self.sourceAddressPrefix = sourceAddressPrefix
        self.destinationAddressPrefix = destinationAddressPrefix
        self.sourceAddressPrefixes = sourceAddressPrefixes
        self.destinationAddressPrefixes = destinationAddressPrefixes
        self.access = access
        self.priority = priority
        self.direction = direction

    #Create an instance of this class given a dictionary of attribute/value pairs
    def createFromDict(self, **kwargs) -> 'SecurityRule':
        lst_attributes = self._get_attribute_list()
        #self.description, self.protocol = [kwargs.get(k) for k in lst_attributes]
        for attribute in lst_attributes:
            self.__setattr__(attribute,kwargs.get(attribute))

        return self.createFromDeepCopy(self)
        #return SecurityRule(self.location, self.nsgname, self.rulename, self.description, self.protocol, self.sourcePortRange, self.destinationPortRange,
            #self.sourceAddressPrefix, self.destinationAddressPrefix, self.access, self.priority, self.direction)

#Create an instance of this class given an OrderedDict object
    def createFromOrderedDict(self, OrderedDict) -> 'SecurityRule':
        lst_attributes = self._get_attribute_list()
        #self.description, self.protocol = [kwargs.get(k) for k in lst_attributes]
        for attribute in lst_attributes:
            self.__setattr__(attribute, OrderedDict[attribute])
        
        return self.createFromDeepCopy(self)
    
    ###
    #Creates and returns a DeepCopy() SecurityRule object based on the one passed
    @classmethod
    def createFromDeepCopy(self, obj:'SecurityRule') -> 'SecurityRule':
        rule = SecurityRule()
        rule.populateAttributes(obj.location, obj.nsgname, obj.rulename, obj.description, obj.protocol, obj.sourcePortRange, obj.destinationPortRange, obj.sourcePortRanges, obj.destinationPortRanges,
            obj.sourceAddressPrefix, obj.sourceAddressPrefixes, obj.destinationAddressPrefix, obj.destinationAddressPrefixes, obj.access, obj.priority, obj.direction)
        return rule



    # ToString for this object
    def __str__(self):
        val_dict = self._get_attribute_value_dictionary()
        lst = []

        for key, val in val_dict.items():
            lst.append(val)
        return ','.join(lst)
    
    ###
    # Returns a list containing all the attributes of this class
    ###
    def _get_attribute_list(self) -> list:
        self_vars = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self,a))]
        return self_vars

    ###
    # Returns a dictionary with attribute name and value
    ###
    def _get_attribute_value_dictionary(self) -> dict:
        #s = locals()["self"]
        var_val = {}
        for attribute in self._get_attribute_list():
            var_val[attribute] = self.__getattribute__(attribute)
        return var_val