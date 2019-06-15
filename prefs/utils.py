'''
    File name: utils.py
    Author/Maintainer: Reuben Cleetus
    email:reuben@cleet.us
    Copyright: 2019
    License: GPL 3.0
    Date last modified: 5/8/2019
    Python Version:3.7
'''

from prefs.prefs import Preferences
import os
from prettytable import PrettyTable
from timeit import default_timer as timer
from decimal import Decimal
from network.securitygroup.nsglist import NSGList

prefs = Preferences()
start = 0.0
end = 0.0
###
# Generates a sample data file to use
def generateSampleDataFile(path) -> bool:
    grouper_file = os.path.join(path, prefs.SAMPLE_DATA_FILE_NAME)
    file_exists = os.path.isfile(grouper_file)
    overwrite_file:str = "n"
    sample_data_file = prefs.load_prefs(prefs.PREFS_SAMPLE_DATA_CONTENTS)
    isFileWritten = False


    if(file_exists == True):
        overwrite_file = input("Sample data file already exists. Overwrite? (y/n) or ENTER to cancel > ")
        if(overwrite_file.lower().startswith("n")):
            return
    
    #Continue to create file
    text_file = open(grouper_file, "w", newline='')
    for line in sample_data_file:
        text_file.write(line + '\n')
    text_file.close()
    isFileWritten = True

    return isFileWritten


###
# Prints output based on the NSGList passed
def printOutputTable(nsglist:NSGList):
    pref = Preferences()
    version = pref.load_prefs("grouper_version")
    version = "<unknown>" if len(version.strip()) == 0 else version
    table = PrettyTable(['NSG Name', 'Resource Group', 'Rules'])
    table.title = f"Grouper v{version}"
    table.align['NSG Name'] = "l"
    table.align['Resource Group'] = "l"
    for key, val in nsglist.nsg_rg_lookup.items():
        num_rules = len(nsglist.nsgDict[key])
        table.add_row([key, val, num_rules])
    print(f"\n\n{table}\n")


###
# Task Timer
def Timed():
    global start
    global end

    if(start == float(0.0)):
        start = timer()
    else:
        end = timer()
        print(f"\nCompleted in {round(Decimal(end - start),5) } milliseconds.")
        start = 0.0
    