import click
from network.securitygroup.securityrule import SecurityRule
from parser.csvparser import CSVParser
from network.securitygroup.nsglist import NSGList
from parser.armwriter import ARMWriter

#from network.networksecuritygroups.securityrule import SecurityRule
#import network.networksecuritygroups.securityrule.SecurityRule

@click.command()
@click.option('--csv', default="grouper-nsg.csv", help='Network Security Rules CSV file to use')
@click.option('--prefs', default=None, help='Grouper preferences json file to use')
@click.option('--genpref', default=None, help='True/False. Generate sample preferences json file')
def doIt(csv, prefs, genpref):


    print("--------")
    parser = CSVParser("/Users/reuben/code/python/Grouper/grouper-sample.csv")
    nsglist = parser.doCSVParse()
    print(nsglist)
    nsglist.printDebug()

    armWriter = ARMWriter()
    arm_template = armWriter.doBuild_Nsg_Template(nsglist.nsgDict)
    print(arm_template)
    armWriter.doWrite_ARMTemplate(arm_template)

doIt()
