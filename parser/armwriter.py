'''
    File name: armwriter.py
    Author/Maintainer: Reuben Cleetus
    email:reuben@cleet.us
    Copyright: 2019
    License: GPL 3.0
    Date last modified: 5/8/2019
    Python Version:3.7
'''
from network.securitygroup.nsglist import NSGList
from network.securitygroup.securityrule import SecurityRule
from pathlib import Path
from collections import defaultdict
import os

class ARMWriter:
    def __init__(self):
        self.FILE_NSGARMTEMPLATE = "nsg_arm_template.txt"
        self.FILE_NSGRULEARMTEMPLATE = "nsgrule_arm_template.txt"
        self.Nsg_Template = str(self.getNSGTemplate())
        self.Nsg_Rule_Template = str(self.getNSGRuleTemplate())
    
    ###
    #Reads and returns the NSG ARM Template file
    def getNSGTemplate(self) -> str:
        os_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(os_path, "../meta/" + self.FILE_NSGARMTEMPLATE)

        file = open(file_path, "r")
        self.Nsg_Template = file.read()
        return self.Nsg_Template
    ###
    #Reads and returns the NSG Rule ARM Template file
    def getNSGRuleTemplate(self) -> str:
        os_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(os_path, "../meta/" + self.FILE_NSGRULEARMTEMPLATE)

        file = open(file_path, "r")
        self.Nsg_Rule_Template = file.read()
        return self.Nsg_Rule_Template
    
    ###
    #Builds and returns a completed the NSG ARM Template
    def doBuild_Nsg_Template(self, nsgList:NSGList) -> {}:
        file_dict = {}
        current_key = ""

        for key, rules in nsgList.items():
            NsgTemplate = self.Nsg_Template
            NsgTemplate = NsgTemplate.replace("%NSGNAME%", key)

            #Loop through each NSG
            if(current_key != key):
                NSGRuleTemplate = ""
                current_key = key
            
            
            idx = 0
            for rule in rules:
                #Loop through each Security Rule
                RuleTemplate = self.Nsg_Rule_Template

                NsgTemplate = NsgTemplate.replace("%LOCATION%", rule.location)
                RuleTemplate = RuleTemplate.replace("%RULENAME%", rule.rulename)
                RuleTemplate = RuleTemplate.replace("%PROTOCOL%", rule.protocol)
                RuleTemplate = RuleTemplate.replace("%SOURCEPORTRANGE%", rule.sourcePortRange)
                RuleTemplate = RuleTemplate.replace("%DESTINATIONPORTRANGE%", rule.destinationPortRange)
                RuleTemplate = RuleTemplate.replace("%SOURCEADDRESSPREFIX%", rule.sourceAddressPrefix)
                RuleTemplate = RuleTemplate.replace("%DESTINATIONADDRESSPREFIX%", rule.destinationAddressPrefix)
                RuleTemplate = RuleTemplate.replace("%ACCESS%", rule.access)
                RuleTemplate = RuleTemplate.replace("%PRIORITY%", rule.priority)
                RuleTemplate = RuleTemplate.replace("%DIRECTION%", rule.direction)
                RuleTemplate = RuleTemplate.replace("%SOURCEPORTRANGES%", rule.sourcePortRanges)
                RuleTemplate = RuleTemplate.replace("%DESTINATIONPORTRANGES%", rule.destinationPortRanges)
                RuleTemplate = RuleTemplate.replace("%SOURCEADDRESSPREFIXES%", rule.sourceAddressPrefixes)
                RuleTemplate = RuleTemplate.replace("%DESTINATIONADDRESSPREFIXES%", rule.destinationAddressPrefixes)

                #Add separator if there's another rule to come
                if( (len(rules) > 1) and idx < (len(rules)-1) ):
                    RuleTemplate = RuleTemplate.replace("%SEPARATOR%", ",")
                else:
                    RuleTemplate = RuleTemplate.replace("%SEPARATOR%", "")
                idx += 1
            
                NSGRuleTemplate = NSGRuleTemplate + '\n' + RuleTemplate

            #Insert RuleTemplate into NSGTemplate
            NsgTemplate = NsgTemplate.replace("%__NSGRULE__%", NSGRuleTemplate)
            
            file_dict[key] = NsgTemplate
        return file_dict
    

    ###
    # Writes each ARM Template out as an individual file  
    def doWrite_ARMTemplate(self, file_dict:defaultdict(list)):
        os_path = os.path.abspath(os.path.dirname(__file__))
        
        for key, val in file_dict.items():
            file_path = os.path.join(os_path, "../output/" + key + ".txt")
            arm_file = open(file_path, "w")
            arm_file.write(val)
            arm_file.close()
        

    

        




    