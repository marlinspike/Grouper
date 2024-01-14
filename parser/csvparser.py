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
from collections import OrderedDict
from prefs.prefs import Preferences
import os
from csv import DictReader
import logging
from logger_config import setup_logger

setup_logger()


class CSVParser:
    """
    A class used to parse CSV files.

    This class contains methods to read and parse CSV files. It is designed to handle CSV files 
    that contain information about Network Security Groups (NSGs) and their rules.

    Attributes:
        filename (str): The name of the CSV file to be parsed.
    """
    def __init__(self, filename):
        self.filename = filename
        self.prefs = Preferences()


    def _doParseToNSGList(self, reader:DictReader) -> NSGList:
        """
        Parses the CSV file to a list of NSGs.

        This method reads the CSV file line by line using the provided DictReader object. For each line, 
        it checks if the priority of the rule is not in the ignore list. If it's not, it creates a new 
        SecurityRule object from the row and adds it to the NSGList. It also updates the NSG resource 
        group lookup dictionary with the NSG name and its corresponding resource group.

        Args:
            reader (DictReader): A DictReader object for reading the CSV file.

        Returns:
            NSGList: A list of NSGs parsed from the CSV file.
        """
        nsglist = NSGList()
        for row in reader:
                #Only add a rule if its priority is not in the Ignore List
                if (not row["priority"] in self.prefs.lst_ignore_priority):
                    rule = SecurityRule().createFromOrderedDict(row)
                    nsglist.addToDict(rule)
                    nsglist.nsg_rg_lookup[row["nsgname"]] = row["resourceGroup"]

        return nsglist



    def doCSVParse(self) -> NSGList:
        """
        Parses the CSV file to populate an NSGList with a SecurityRule object for each row.

        This method opens the CSV file, reads it using a DictReader object, and then calls the 
        `_doParseToNSGList` method to parse the CSV data into an NSGList.

        Returns:
            NSGList: A list of NSG objects with their corresponding SecurityRule objects.
        """
        nsglist = NSGList()
        with open(self.filename) as csvFile:
            reader = csv.DictReader(csvFile)

            nsglist = self._doParseToNSGList(reader)
        return nsglist


    def reorderDict(self, dict) -> OrderedDict:
        """
        Parses the CSV file to populate an NSGList with a SecurityRule object for each row.

        This method opens the CSV file, reads it using a DictReader object, and then calls the 
        `_doParseToNSGList` method to parse the CSV data into an NSGList.

        Returns:
            NSGList: A list of NSG objects with their corresponding SecurityRule objects.
        """
        preferredOrder = Preferences().load_prefs("preferred_order").split(",")
        oDict = OrderedDict([item, ''] for item in preferredOrder) 

        for item in preferredOrder:
            oDict[item] = dict.get(item)

        return oDict


    def writeCSVFromNSGList(self, nsgList:NSGList, path:str) -> bool:
        """
        Writes a Grouper CSV file from an NSG list.

        This method generates a CSV file from the provided NSG list. Each row in the CSV file corresponds to a 
        SecurityRule object in the NSG list. The columns of the CSV file are the attributes of the SecurityRule 
        objects, in the order specified by the "preferred_order" preference.

        Args:
            nsgList (NSGList): A list of NSGs, each with its associated rules.
            path (str): The path where the CSV file should be written.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        os_path = os.path.abspath(os.path.dirname(__file__))
        grouper_file = os.path.join(path, self.filename)

        with open(grouper_file, 'w') as gFile:
            lstAttrs = SecurityRule()._get_attribute_list()
            lstAttrs.append("resource_group")
            gWriter = csv.DictWriter(gFile, fieldnames = lstAttrs)
            gWriter.writeheader()

            for nsgName in nsgList.nsgDict:
                for rule in nsgList.nsgDict[nsgName]:
                    dict = self.reorderDict(rule.toDict())
                    gWriter.writerow(dict)
    


