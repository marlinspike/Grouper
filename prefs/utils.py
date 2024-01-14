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
from timeit import default_timer as timer
from decimal import Decimal
from network.securitygroup.nsglist import NSGList
from rich.table import Table
from rich.console import Console
import logging
from logger_config import setup_logger

setup_logger()

prefs = Preferences()
start = 0.0
end = 0.0

def generateSampleDataFile(path) -> bool:
    """
    Generates a sample data file at the specified path.

    Args:
        path (str): The path where the sample data file should be created.

    Returns:
        bool: True if the file was successfully written, False otherwise.
    """
    grouper_file = os.path.join(path, prefs.SAMPLE_DATA_FILE_NAME)
    file_exists = os.path.isfile(grouper_file)
    overwrite_file:str = "n"
    sample_data_file = prefs.load_prefs(prefs.PREFS_SAMPLE_DATA_CONTENTS)
    isFileWritten = False

    if(file_exists == True):
        overwrite_file = input("Sample data file already exists. Overwrite? (y/n) or ENTER to cancel > ")
        if(overwrite_file.lower().startswith("n")):
            logging.info("User chose not to overwrite existing sample data file.")
            return
    
    #Continue to create file
    text_file = open(grouper_file, "w", newline='')
    for line in sample_data_file:
        text_file.write(line + '\n')
    text_file.close()
    isFileWritten = True

    logging.info(f"Sample data file {grouper_file} has been created.")

    return isFileWritten



def printOutputTable(nsglist:NSGList):
    """
    Generates a sample data file at the specified path.

    Args:
        path (str): The path where the sample data file should be created.

    Returns:
        bool: True if the file was successfully written, False otherwise.
    """
    pref = Preferences()
    version = pref.load_prefs("grouper_version")
    version = "<unknown>" if len(version.strip()) == 0 else version

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.title = f"Grouper v{version}"
    table.add_column('NSG Name', justify="left")
    table.add_column('Resource Group', justify="left")
    table.add_column('Rules')

    for key, val in nsglist.nsg_rg_lookup.items():
        num_rules = len(nsglist.nsgDict[key])
        table.add_row(key, val, str(num_rules))

    console.print(table)


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
    