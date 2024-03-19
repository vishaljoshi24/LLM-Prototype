import pandas as pd
import os


# Returns a list of all chatlog text files
def list_chatlogs():
    return [f for f in os.listdir("../files/chatlogs") if f.endswith(".txt")]


# Converts a chatlog text file to a dataframe
# Accepts chatlog id or file name
def chatlog_to_df(chatlog):
    # If only id is given, adds file extension
    if not chatlog.endswith(".txt"):
        chatlog = chatlog + ".txt"
    # If the file does not exist, returns an empty dataframe
    if not os.path.isfile("files/chatlogs/" + chatlog):
        df = pd.DataFrame()
    # If file exists, creates dataframe from standard chatlog format
    else:
        df = pd.read_csv(
            "files/chatlogs/" + chatlog, sep=":", header=None, names=["From", "Message"]
        )
    return df


# Creates a list of all chatlogs as dataframes
def all_chatlogs_to_df():
    df_list = []
    for i in list_chatlogs():
        df_list.append(chatlog_to_df(i))
    return df_list
