import numpy as np
import scipy
import pandas as pd
import re

def group_ids(df):
    """Function for grouping up messages by unique identifier

    Args:
        df (pandas dataframe): dataframe that contains board dataset

    Returns:
        dict: dictionary with sorted ids and corresponding messages for each id
    """

    print("Grouping ids")

    #getting unique ids
    unique_ids = df["id"].unique()

    #creating a grouped dictionary
    grouped_ids = {}

    #extracting messages based on the id
    for u_id in unique_ids:
        #extracting values for the given unique id
        p_vals = df.loc[df["id"] == u_id]
        #adding values to the dictionary
        grouped_ids[u_id] = p_vals["com"].tolist()

    #return
    return grouped_ids

def load_data(dataset_path):
    """Dataset loading function. Uses pandas to load csv file from a given path.

    Args:
        dataset_path (str): path to csv file

    Returns:
        dataframe: pandas dataframe containing board dataset
    """
    print("Loading data")
    #returning
    return pd.read_csv(dataset_path, index_col='thread_num')

def id_metadata(grouped_ids):
    """Function for printing data of the key with most messages

    Args:
        grouped_ids (dict): dictionary with all ids and all the messages associated with them

    Returns:
        string: key with most messages
    """
    print("Grouped ids max key length")
    max_key = max(grouped_ids, key=lambda x: len(set(grouped_ids[x])))
    print(max_key)
    print(len(grouped_ids[max_key]))
    print(grouped_ids[max_key])
    return max_key
    
def main():

    print("Start")
    #loading data
    df = load_data('dataset/pol_2020-8-12_14-13.csv')
    grouped_ids = group_ids(df)
    max_id = id_metadata(grouped_ids)



if __name__ == "__main__":
    main()