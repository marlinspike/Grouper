from prefs.prefs import Preferences
import os

prefs = Preferences()

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