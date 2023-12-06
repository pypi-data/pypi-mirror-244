# importing the modules
from datetime import datetime
import pandas as pd
import csv
import json

directoryPathToFilesOfResults = ""

pd.options.display.max_rows = 999
pd.options.display.max_columns = 999
def read_csv_file(file_path):
    """Read a CSV file and return the DataFrame."""
    return pd.read_csv(file_path, sep=';')

def representsInt(s):
    """Function to test if a string is an int"""
    try:
        int(s)
        return True
    except ValueError:
        return False


def representsFloat(s):
    """Function to test if a string is a float"""
    try:
        float(s)
        return True
    except ValueError:
        return False


def getListAverageOrNegative1(listOfValues):
    """Return average from a list or return a default value -1"""
    if len(listOfValues):
        return sum(listOfValues) / len(listOfValues)
    else:
        return -1


def refactorUserLog_UnfilteredJSON_TO_FilteredDict(stringUserLogResultsUnfiltered):
    """String split to analyse the results of the userLog, that come in a very unfiltered state. The intended form is JSON, but the userLog captured clicked html nodes that interefered with the JSON format (such as the ' character).
    The following lines contains the pattern to be applied.
    First it must be chosen a special character with low probability of existing in the string (such as 'Ç').
    To make sure it is safe to proceed, replace existing (if there are) 'ç' with other character."""

    # Make string split of stringUserLogResultsUnfiltered on "{"userInfo":" and include this substring to the prefix of the return parameter.
    stringUserLog = stringUserLogResultsUnfiltered.split("{'userInfo':")[1]
    stringUserLog = "{'userInfo':" + stringUserLog

    # Ç->::::: #replace existing 'Ç' with other unusual character, so we can start fixing the JSON file
    stringUserLog = stringUserLog.replace("Ç", ":::::")
    # 'node': ""->ÇnodeÇ: Ç
    stringUserLog = stringUserLog.replace("\'node\': \"\"", "ÇnodeÇ: Ç")
    # ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    stringUserLog = stringUserLog.replace(
        ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",
        " ")
    # '\n'->''
    stringUserLog = stringUserLog.replace('\n', '')
    # '"""'->''
    stringUserLog = stringUserLog.replace('\"\"\"', '')
    # '"",'->'Ç.'
    stringUserLog = stringUserLog.replace('</strong>\"\",', '</strong>Ç,')
    # p>"",->Ç,
    stringUserLog = stringUserLog.replace("p>\"\",", "p>Ç,")
    # {'->{Ç
    stringUserLog = stringUserLog.replace("{'", "{Ç")
    # '}->Ç}
    stringUserLog = stringUserLog.replace("'}", "Ç}")
    # ':->Ç:
    stringUserLog = stringUserLog.replace("':", "Ç:")
    #: '->: Ç
    stringUserLog = stringUserLog.replace(": '", ": Ç")
    # ',->Ç,
    stringUserLog = stringUserLog.replace("',", "Ç,")
    # , '->, Ç
    stringUserLog = stringUserLog.replace(", '", ", Ç")
    # ";->
    stringUserLog = stringUserLog.replace("\";", " ")
    # "" '""
    stringUserLog = stringUserLog.replace("\"\"\'\"\"", "null")
    # "->null
    stringUserLog = stringUserLog.replace("\"", "null")
    # \->;;;;;
    stringUserLog = stringUserLog.replace("\\", ";;;;;")

    # Ç->" #Finally convert the special character that we introduced to refactor the JSON ('Ç') with the double quotes ('"') so we can finish fixing the JSON
    stringUserLog = stringUserLog.replace("Ç", "\"")

    return json.loads(stringUserLog)


def getMicroTaskSpecificClickDetailsCount(userLogDict):
    """From the userLogDict (user interactions records, e.g. click details or key presses), it is obtained the click details.
    The task fingerprinting is analysed into three variables:
    ->hesitant actions (e.g. counting microtask - change the input values; taking too much time with an higher timestamp inside microtasks);
    ->confident actions (few key presses with lower timestamp inside microtasks);
    ->hurry actions (actions too fast which may indicate that the user wants to spam the microtask)

    There are another actions that it could be analyzed, such as:
    ->(TODO) cheating or lazy actions (has the same key press, which may trick the cognitive tests because of the random display trials);
    ->(TODO) erroneous keypresses inside or outside interface;SEE COGNITIVE TESTS/MICROTASKS THAT ARE BASED ON CLICK DETAILS BUT INSTEAD USERS ERRONEOUSLY KEY PRESSES!

     """
    trialElementFinalResultClickDetails = {}
    if len(userLogDict['clicks']['clickDetails']) > 0:
        # In this loop, it will iterate on each click object to identify the task fingerprinting actions
        clickDetailsList = []
        hesitantActions = 0
        confidentActions = 0
        hurryActions = 0
        specialActions = 0
        for clickDetail in userLogDict['clicks']['clickDetails'][0:]:
            clickDetailsList.append(clickDetail)
            if (clickDetail['timestamp'] < 100):
                hurryActions = hurryActions + 1
            elif (clickDetail['timestamp'] < 10000):
                confidentActions = confidentActions + 1
            else:
                hesitantActions = hesitantActions + 1

        trialElementFinalResultClickDetails = {"lenClickDetails": len(clickDetailsList), "hurryActions": hurryActions,
                                               "confidentActions": confidentActions, "hesitantActions": hesitantActions,
                                               "specialActions": specialActions}

    return trialElementFinalResultClickDetails


def getMicroTaskSpecificKeyPressCount(userLogDict):
    """
    Similar functioning of the method 'getMicroTaskSpecificClickDetailsCount', but this time focus on the keyboard presses instead of the click details.

    The task fingerprinting is analysed into three variables:
    ->hesitant actions (e.g. counting microtask - change the input values; taking too much time with an higher timestamp inside microtasks);
    ->confident actions (few key presses with lower timestamp inside microtasks);
    ->hurry actions (actions too fast which may indicate that the user wants to spam the microtask)
    ->special keys or special actions (e.g. CNTRL + C or change focus to other inputs or even other browser tabs)

    There are another actions that it could be analyzed, such as:
    ->(TODO) cheating or lazy actions (has the same key press, which may trick the cognitive tests because of the random display trials);
    ->(TODO) erroneous keypresses inside or outside interface;SEE COGNITIVE TESTS/MICROTASKS THAT ARE BASED ON CLICK DETAILS BUT INSTEAD USERS ERRONEOUSLY KEY PRESSES!
    """
    trialElementFinalResultKeyDetails = {}
    if len(userLogDict['keyLogger']) > 0:
        # In this loop, it will iterate on each key press object to identify the task fingerprinting actions
        keyDetailsList = []
        hesitantActions = 0
        confidentActions = 0
        hurryActions = 0
        specialActions = 0
        for keyDetail in userLogDict['keyLogger'][0:]:
            keyDetailsList.append(keyDetail)
            if (keyDetail['timestamp'] < 100):
                hurryActions = hurryActions + 1
            elif (keyDetail['timestamp'] < 10000):
                confidentActions = confidentActions + 1
            else:
                hesitantActions = hesitantActions + 1

                listSpecialKeys = ["x11", "x10", "x08", "x12", "Â>>"]

                if any(x in str(keyDetail['data']) for x in listSpecialKeys):
                    specialActions = specialActions + 1

        trialElementFinalResultKeyDetails = {"lenClickDetails": len(keyDetailsList), "hurryActions": hurryActions,
                                             "confidentActions": confidentActions,
                                             "hesitantActions": hesitantActions, "specialActions": specialActions}

    return trialElementFinalResultKeyDetails

def main():
    # User input for the path files with the results to be processed and applied the task fingerprinting technique
    listPathFileResults= input("Enter the paths for the files with the results, separated by commas: ").split(',')

    for filename in listPathFileResults:
        # code starts here to fetch each  results file and then normalize the data towards a single file.
        df = pd.read_json(filename)
        now = datetime.now()
        date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
        df.to_csv(r'export_dataframe_workshop_' + date_time + '.csv', sep=";", index=False, header=True)
        file = open(filename, "r", encoding="utf8")

        userLogDict = refactorUserLog_UnfilteredJSON_TO_FilteredDict(file.read())

        clickTaskFingerprintingDict = getMicroTaskSpecificClickDetailsCount(userLogDict)
        keyTaskFingerprintingDict = getMicroTaskSpecificClickDetailsCount(userLogDict)

        with open(r'resultsTaskFingerprintingClickDetails'+datetime+'.csv', 'w', newline='') as outputfile:
            # saves the results of the click details in a csv file
            if clickTaskFingerprintingDict is not None:
                keys = clickTaskFingerprintingDict.keys()
                dict_writer = csv.DictWriter(outputfile, keys, delimiter=";")
                dict_writer.writeheader()
                dict_writer.writerows(clickTaskFingerprintingDict)

        with open(r'resultsTaskFingerprintingKeyDetails'+datetime+'.csv', 'w', newline='') as outputfile:
            # saves the results of the key details in a csv file
            if keyTaskFingerprintingDict is not None:
                keys = keyTaskFingerprintingDict.keys()
                dict_writer = csv.DictWriter(outputfile, keys, delimiter=";")
                dict_writer.writeheader()
                dict_writer.writerows(clickTaskFingerprintingDict)


if __name__ == "__main__":
    main()