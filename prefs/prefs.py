'''
    File name: prefs.py
    Author/Maintainer: Reuben Cleetus
    email:reuben@cleet.us
    Copyright: 2019
    License: GPL 3.0
    Date last modified: 5/8/2019
    Python Version:3.7
'''
import sys
import json
import os
from datetime import datetime
import logging
from logger_config import setup_logger

setup_logger()

class Preferences:
    """
        A class used to manage preferences for the application.

        This class contains methods to load preferences from a JSON file. It also contains attributes that represent 
        various preferences, such as a list of priority numbers to ignore, the name of a sample data file, and the 
        contents of the sample data.

        Attributes:
            lst_ignore_priority (list): A list of priority numbers to ignore.
            sample_file (str): The name of a sample data file.
            SAMPLE_DATA_FILE_NAME (str): The constant name of the sample data file.
            PREFS_SAMPLE_DATA_CONTENTS (str): The constant name for the preference that contains the contents of the sample data.
    """
    def __init__(self):
        self.lst_ignore_priority = []; [65000, 65001, 65500] #Reserved numbers in Azure. Do not reuse
        self.lst_ignore_priority = self.load_prefs('ignore_priority').split(",")
        self.sample_file = ""
        self.SAMPLE_DATA_FILE_NAME = "grouper-sample.csv"
        self.PREFS_SAMPLE_DATA_CONTENTS = "sample_data_contents"
    

    def load_prefs(self, prefName) -> str:
        """
        Loads a specific preference from the preferences file.

        This method reads the preferences file, which is a JSON file located in the same directory as this script. 
        It then returns the value of the specified preference.

        Args:
            prefName (str): The name of the preference to load.

        Returns:
            str: The value of the specified preference.

        Raises:
            SystemExit: If there is an issue reading the preferences file, the script will exit with a status code of 200.
        """
        os_path = os.path.abspath(os.path.dirname(__file__))
        prefsFile = os.path.join(os_path, "prefs.json")
        preference = ""

        try:
            with open(prefsFile) as cred_data:
                prefs = json.load(cred_data)
                preference = prefs[prefName]
        except Exception as e:
            msg = 'There was an issue reading in the credentials file ' + prefsFile
            print(msg)
            print('[ERROR] ' + str(e))
            sys.exit(200)

        return preference


    

