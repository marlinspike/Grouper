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
import logging
from logger_config import setup_logger

setup_logger()

class ARMWriter:
    """
    A class used to handle Azure Resource Manager (ARM) templates for Network Security Groups (NSGs) and NSG rules.

    Attributes:
        FILE_NSGARMTEMPLATE (str): The filename of the NSG ARM template.
        FILE_NSGRULEARMTEMPLATE (str): The filename of the NSG rule ARM template.
        Nsg_Template (str): The content of the NSG ARM template.
        Nsg_Rule_Template (str): The content of the NSG rule ARM template.
    """
    def __init__(self):
        """
        The constructor for ARMWriter class.

        Initializes the filenames of the NSG and NSG rule ARM templates, and stores their content.
        """
        self.FILE_NSGARMTEMPLATE = "nsg_arm_template.txt"
        self.FILE_NSGRULEARMTEMPLATE = "nsgrule_arm_template.txt"
        self.Nsg_Template = str(self.getNSGTemplate())
        self.Nsg_Rule_Template = str(self.getNSGRuleTemplate())
    
    def getNSGTemplate(self) -> str:
        """
        Reads and returns the NSG ARM Template file.

        This method reads the NSG ARM Template file from the relative path "../meta/", 
        stores its content in the instance variable `self.Nsg_Template`, and returns the content.

        Returns:
            str: The content of the NSG ARM Template file.
        """
        os_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(os_path, "../meta/" + self.FILE_NSGARMTEMPLATE)

        file = open(file_path, "r")
        self.Nsg_Template = file.read()
        return self.Nsg_Template


    def getNSGRuleTemplate(self) -> str:
        """
        Reads and returns the NSG Rule ARM Template file.

        This method reads the NSG Rule ARM Template file from the relative path "../meta/", 
        stores its content in the instance variable `self.Nsg_Rule_Template`, and returns the content.

        Returns:
            str: The content of the NSG Rule ARM Template file.
        """
        os_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(os_path, "../meta/" + self.FILE_NSGRULEARMTEMPLATE)

        file = open(file_path, "r")
        self.Nsg_Rule_Template = file.read()
        return self.Nsg_Rule_Template
    

    def doBuild_Nsg_Template(self, nsgList:NSGList) -> {}:
        """
        Builds the NSG Template by replacing placeholders with actual values.

        This method iterates over the provided NSG list, replacing placeholders in the NSG and NSG Rule templates
        with actual values for each NSG and its rules. It maintains a dictionary mapping each NSG to its corresponding
        filled template.

        Args:
            nsgList (NSGList): A list of NSGs, each with its associated rules.

        Returns:
            dict: A dictionary mapping each NSG to its corresponding filled template.
        """
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
    


    def doWrite_ARMTemplate(self, file_dict:defaultdict(list)) -> bool:
        """
        Writes the ARM templates to files.

        This method iterates over the provided dictionary, writing each value to a file with the corresponding key as its name.
        The files are written to the relative path "../output/". If this directory does not exist, it is created.

        Args:
            file_dict (defaultdict(list)): A dictionary mapping file names to their corresponding ARM templates.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        os_path = os.path.abspath(os.path.dirname(__file__))
        isDone = True

        try:
            for key, val in file_dict.items():
                file_dir = os.path.join(os_path, "../output/")
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                file_path = os.path.join(file_dir + key + ".txt")
                with open(file_path, "w") as arm_file:
                    arm_file.write(val)
        except:
            isDone = False
        
        return isDone

    

        




    