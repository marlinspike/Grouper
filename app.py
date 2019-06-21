#!/usr/bin/env python
__author__ = "Reuben Cleetus"
__copyright__ = "Copyright 2019"
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Reuben Cleetus"
__email__ = "reuben@cleet.us"
__status__ = "Production"
'''
    File name: app.py
    Author/Maintainer: Reuben Cleetus
    email:reuben@cleet.us
    Copyright: 2019
    License: GPL 3.0
    Date last modified: 5/8/2019
    Python Version:3.7
'''

import click
from network.securitygroup.securityrule import SecurityRule
from parser.csvparser import CSVParser
from network.securitygroup.nsglist import NSGList
from parser.armwriter import ARMWriter
from parser.cliwriter import CLIWriter
from prefs import utils
import os
import sys
from prettytable import PrettyTable
from prefs.prefs import Preferences
import time
from timeit import default_timer as timer
from decimal import Decimal
from parser.jsonParser import JSONParser

@click.group()
def main():
    pass

@main.command()
@click.option('--csvfile', default="grouper.csv", help='Build Mode: Name the CSV File that Grouper will build from your NSG Rules')
def aznsg(csvfile):
    utils.Timed()

    prefs = Preferences()
    os_path = os.path.abspath(os.path.dirname(__file__))
    

    # Build NSG list from AzCLI Json doc
    try:
        Az = JSONParser().parseAzureAccountJson()
        print(f"Importing NSGs from Azure:\nAccount: {Az['name']}\nEnvironment: {Az['environmentName']}")
        nsglist = JSONParser().parseJson()
        grouper_file = os.path.join(os_path, csvfile)
        CSVParser(csvfile).writeCSVFromNSGList(nsglist, os_path)
        utils.printOutputTable(nsglist)
    
        print(f"Successfully imported NSG Rules from Azure to file [{csvfile}]!")
    except:
        print("An error occurred while accessing Azure. Please verify your Azure CLI installation, or your current login with Azure CLI (use 'az login') before continuing.")

    utils.Timed()
#doIt()


#Writes arm templates based upon the CSV datafile passed
@main.command()
@click.option('--csvfile', default="", help='CSV data file to use')
def csvtoarm(csvfile):
    utils.Timed()
    os_path = os.path.abspath(os.path.dirname(__file__))
    #Parse datafile if provided
    if(len(csvfile) > 0):
        grouper_file = os.path.join(os_path, csvfile)
        file_exists = os.path.isfile(grouper_file)
        if(file_exists == False):
                print(f"Error: There was an error reading in the data file {csvfile}.\n\nPlease use the --genfile option to generate a sample data file to customize.")
                sys.exit(200)

        parser = CSVParser(grouper_file)
        nsglist = parser.doCSVParse()

        armWriter = ARMWriter()
        arm_template = armWriter.doBuild_Nsg_Template(nsglist.nsgDict)
        if (armWriter.doWrite_ARMTemplate(arm_template)):
            utils.printOutputTable(nsglist)
            print(f"Successfully created output ARM Templates in [output] directory for each NSG!")
    utils.Timed()


#Generates CLI file from CSV
@main.command()
@click.option('--csvfile', default="", help='CSV data file to use')
@click.option('--clifile', default="cliFile.cli", help='CSV data file to use')
def csvtocli(csvfile, clifile):
    utils.Timed()
    os_path = os.path.abspath(os.path.dirname(__file__))
    #Parse datafile if provided
    if(len(csvfile) > 0):
        grouper_file = os.path.join(os_path, csvfile)
        file_exists = os.path.isfile(grouper_file)
        if(file_exists == False):
                print(f"Error: There was an error reading in the data file {csvfile}.\n\nPlease use the --genfile option to generate a sample data file to customize.")
                sys.exit(200)

        parser = CSVParser(grouper_file)
        nsglist = parser.doCSVParse()

        cliWriter = CLIWriter(clifile)
        if (cliWriter.doWrite_CLIScript(nsglist.nsgDict,os.path.abspath(os.path.dirname(__file__)))):
            utils.printOutputTable(nsglist)
            print(f"Successfully created CLI Scripts in [output] directory for each NSG!")
    utils.Timed()


#Generates the sample Grouper CSV File
@main.command()
def generatecsv():
    os_path = os.path.abspath(os.path.dirname(__file__))

    if(utils.generateSampleDataFile(os_path)):
        print(f"Sample data file generated! You can customize it, or generate templates based on the sample data.")
    else:
        print("Aborted writing file template.")
    sys.exit(200)



if __name__ == '__main__':
    main()