import sys
import json
import os
from datetime import datetime

class Preferences:

    def __init__(self):
        self.lst_ignore_priority = []; [65000, 65001, 65500] #Reserved numbers in Azure. Do not reuse
        self.lst_ignore_priority = self.load_prefs('ignore_priority').split(",")
        self.sample_file = ""
        self.SAMPLE_DATA_FILE_NAME = "grouper-sample.csv"
        self.PREFS_SAMPLE_DATA_CONTENTS = "sample_data_contents"
    
    ###
    # Loads preferences
    def load_prefs(self, prefName) -> str:
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


    

