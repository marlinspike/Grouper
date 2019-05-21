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
from prefs import utils
import os
import sys
from prettytable import PrettyTable
from prefs.prefs import Preferences
from progress.bar import ShadyBar
import time
from timeit import default_timer as timer
from decimal import Decimal

@click.command()
@click.option('--datafile', default="grouper-sample.csv", help='CSV data file to use')
@click.option('--genfile/--nogen', default=False, help='True/False. Generate sample preferences json file')
def doIt(datafile, genfile):
    start = timer()

    prefs = Preferences()
    
    os_path = os.path.abspath(os.path.dirname(__file__))
    
    if(genfile == True):
        if(utils.generateSampleDataFile(os_path)):
            print(f"Sample data file generated! You can customize it, or generate templates based on the sample data.")
        else:
            print("Aborted writing file template.")
        sys.exit(200)

    
    
    grouper_file = os.path.join(os_path, datafile)
    file_exists = os.path.isfile(grouper_file)
    if(file_exists == False):
            print(f"Error: There was an issue reading in the data file {datafile}.\n\nPlease use the --genfile option to generate a sample data file to customize.")
            sys.exit(200)

    parser = CSVParser(grouper_file)
    nsglist = parser.doCSVParse()

    armWriter = ARMWriter()
    arm_template = armWriter.doBuild_Nsg_Template(nsglist.nsgDict)
    armWriter.doWrite_ARMTemplate(arm_template)

    end = timer()
    print(f"\nCompleted in {round(Decimal(end - start),5) } milliseconds.")

    utils.printOutputTable(nsglist)

doIt()
