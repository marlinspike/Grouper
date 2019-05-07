import click
from network.securitygroup.securityrule import SecurityRule
from parser.csvparser import CSVParser
from network.securitygroup.nsglist import NSGList
from parser.armwriter import ARMWriter
import os
import sys
from prefs.prefs import Preferences


@click.command()
@click.option('--datafile', default="grouper-sample.csv", help='CSV data file to use')
@click.option('--genfile/--nogen', default=False, help='True/False. Generate sample preferences json file')
def doIt(datafile, genfile):


    print("--------")
    prefs = Preferences()
    os_path = os.path.abspath(os.path.dirname(__file__))
    
    if(genfile == True):
        prefs.generateSampleDataFile(os_path)
        print(f"Sample data file generated! You can customize it, or generate templates based on the sample data.")
        sys.exit(200)

    
    
    grouper_file = os.path.join(os_path, datafile)
    file_exists = os.path.isfile(grouper_file)
    if(file_exists == False):
            print(f"Error: There was an issue reading in the data file {datafile}.\n\nPlease use the --genfile option to generate a sample data file to customize.")
            sys.exit(200)

    parser = CSVParser(grouper_file)
    nsglist = parser.doCSVParse()
    print(nsglist.nsg_rg_lookup)

    armWriter = ARMWriter()
    arm_template = armWriter.doBuild_Nsg_Template(nsglist.nsgDict)
    armWriter.doWrite_ARMTemplate(arm_template)

doIt()
