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
from rich.console import Console
import logging
from logger_config import setup_logger

setup_logger()

@click.group()
def main():
    """Main function that groups the CLI commands."""
    pass

@main.command()
@click.option('--csvfile', default="grouper.csv", help='Build Mode: Name the CSV File that Grouper will build from your NSG Rules')
def aznsg(csvfile):
    """
    Function to build NSG list from AzCLI Json doc.
    
    Args:
        csvfile (str): The name of the CSV file that Grouper will build from your NSG Rules.
    """
    logging.info("Started aznsg")    
    utils.Timed()

    prefs = Preferences()
    os_path = os.path.abspath(os.path.dirname(__file__))
    
    # Create a Console object for pretty printing
    console = Console()

    # Build NSG list from AzCLI Json doc
    try:
        Az = JSONParser().parseAzureAccountJson()
        console.print(f"Importing NSGs from Azure:\nAccount: {Az['name']}\nEnvironment: {Az['environmentName']}", style="bold green")
        logging.info(f"Importing NSGs from Azure:\nAccount: {Az['name']}\nEnvironment: {Az['environmentName']}")
        nsglist = JSONParser().parseJson()
        grouper_file = os.path.join(os_path, csvfile)
        CSVParser(csvfile).writeCSVFromNSGList(nsglist, os_path)
        utils.printOutputTable(nsglist)
    
        console.print(f"Successfully imported NSG Rules from Azure to file [{csvfile}]!", style="bold green")
        logging.info(f"Successfully imported NSG Rules from Azure to file [{csvfile}]!")
    except Exception as e:
        console.print("An error occurred while accessing Azure. Please verify your Azure CLI installation, or your current login with Azure CLI (use 'az login') before continuing.", style="bold red")
        logging.error("An error occurred while accessing Azure. Please verify your Azure CLI installation, or your current login with Azure CLI (use 'az login') before continuing.")
    utils.Timed()
#doIt()


#Writes arm templates based upon the CSV datafile passed
@main.command()
@click.option('--csvfile', default="", help='CSV data file to use')
def csvtoarm(csvfile):
    """
    Function to write ARM templates based upon the CSV data file passed.
    
    Args:
        csvfile (str): The CSV data file to use.
    """
    logging.info("Started csvtoarm")
    utils.Timed()
    os_path = os.path.abspath(os.path.dirname(__file__))
    
    # Create a Console object for pretty printing
    console = Console()

    # Parse datafile if provided
    if(len(csvfile) > 0):
        grouper_file = os.path.join(os_path, csvfile)
        file_exists = os.path.isfile(grouper_file)
        if(file_exists == False):
            console.print(f"Error: There was an error reading in the data file {csvfile}.\n\nPlease use the --genfile option to generate a sample data file to customize.", style="bold red")
            logging.error(f"Error: There was an error reading in the data file {csvfile}.\n\nPlease use the --genfile option to generate a sample data file to customize.")
            sys.exit(200)

        parser = CSVParser(grouper_file)
        nsglist = parser.doCSVParse()

        armWriter = ARMWriter()
        arm_template = armWriter.doBuild_Nsg_Template(nsglist.nsgDict)
        if (armWriter.doWrite_ARMTemplate(arm_template)):
            utils.printOutputTable(nsglist)
            console.print(f"Successfully created output ARM Templates in [output] directory for each NSG!", style="bold green")
            logging.info(f"Successfully created output ARM Templates in [output] directory for each NSG!")
    utils.Timed()


#Generates CLI file from CSV
@main.command()
@click.option('--csvfile', default="", help='CSV data file to use')
@click.option('--clifile', default="cliFile.cli", help='CSV data file to use')
def csvtocli(csvfile, clifile):
    """
    Function to generate CLI file from CSV.
    
    Args:
        csvfile (str): The CSV data file to use.
        clifile (str): The CLI file to generate.
    """
    logging.info("Started csvtocli")
    utils.Timed()
    os_path = os.path.abspath(os.path.dirname(__file__))
    
    # Create a Console object for pretty printing
    console = Console()

    # Parse datafile if provided
    if(len(csvfile) > 0):
        grouper_file = os.path.join(os_path, csvfile)
        file_exists = os.path.isfile(grouper_file)
        if(file_exists == False):
            console.print(f"Error: There was an error reading in the data file {csvfile}.\n\nPlease use the --genfile option to generate a sample data file to customize.", style="bold red")
            logging.error(f"Error: There was an error reading in the data file {csvfile}.\n\nPlease use the --genfile option to generate a sample data file to customize.")
            sys.exit(200)

        parser = CSVParser(grouper_file)
        nsglist = parser.doCSVParse()

        cliWriter = CLIWriter(clifile)
        if (cliWriter.doWrite_CLIScript(nsglist.nsgDict,os.path.abspath(os.path.dirname(__file__)))):
            utils.printOutputTable(nsglist)
            console.print(f"Successfully created CLI Scripts in [output] directory for each NSG!", style="bold green")
            logging.info(f"Successfully created CLI Scripts in [output] directory for each NSG!")
    utils.Timed()


#Generates the sample Grouper CSV File
@main.command()
def generatecsv():
    """
    Function to generate the sample Grouper CSV File.
    """
    logging.info("Started generatecsv")
    os_path = os.path.abspath(os.path.dirname(__file__))
    
    # Create a Console object for pretty printing
    console = Console()

    if(utils.generateSampleDataFile(os_path)):
        console.print("Sample data file generated! You can customize it, or generate templates based on the sample data.", style="bold green")
        logging.info("Sample data file generated! You can customize it, or generate templates based on the sample data.")
    else:
        console.print("Aborted writing file template.", style="bold red")
        logging.error("Aborted writing file template.")
    sys.exit(200)



if __name__ == '__main__':
    main()