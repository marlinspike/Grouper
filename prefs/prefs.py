import sys
import json
import os
from datetime import datetime

class Preferences:

    def __init__(self):
        self.lst_ignore_priority = []; [65000, 65001, 65500] #Reserved numbers in Azure. Do not reuse
        self.lst_ignore_priority = self.load_prefs('ignore_priority').split(",")
        self.sample_file = ""
    
    ###
    # Loads preferences
    def load_prefs(self, prefName) -> str:
        os_path = os.path.abspath(os.path.dirname(__file__))
        prefsFile = os.path.join(os_path, "prefs.json")
        preference = ""

        #prefsFile = './prefs.json'
        today = datetime.now().strftime('%Y-%m-%d')
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


    ###
    # Generates a sample data file to use
    def generateSampleDataFile(self, path):
        grouper_file = os.path.join(path, "grouper-sample.csv")
        file_exists = os.path.isfile(grouper_file)
        overwrite_file:str = "n"
        sample_data_file = self.load_prefs('sample_data_file')


        if(file_exists == True):
            overwrite_file = input("Sample data file already exists. Overwrite? (y/n) or ENTER to cancel > ")
            if(overwrite_file.lower().startswith("n")):
                return
        
        #Continue to create file
        text_file = open(grouper_file, "w", newline='')
        for line in sample_data_file:
            text_file.write(line + '\n')
        text_file.close()

