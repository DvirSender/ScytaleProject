import pandas as pd
import os


# Function to create an empty dictionary with specific keys
def create_empty_data_dict():
    data_dict = {
        "Organization Name": [],
        "repository_id": [],
        "repository_name": [],
        "repository_owner": [],
        "num_prs": [],
        "num_prs_merged": [],
        "merged_at": [],
        "is_compliant": []
    }
    return data_dict


# Function to merge two dataframes
def merge_dataframes(dataframe1, dataframe2):
    merged_df = pd.concat([dataframe1, dataframe2])
    return merged_df


# Function to transform JSON files into a dataframe
def transform_json_files_to_df(files_list):
    result_df = pd.DataFrame(create_empty_data_dict())
    for file in files_list:
        if file == []:
            continue
        empty_data_dict = create_empty_data_dict()
        filled_df = fill_data_dict_from_file(empty_data_dict, file)
        if result_df.empty:
            result_df = filled_df
        else:
            result_df = merge_dataframes(result_df, filled_df)
    return result_df


# Function to list all files in the data directory
def get_files_in_data_directory():
    files_list = os.listdir("github_data")
    return files_list


# Function to fill the dictionary with data from the JSON file
def fill_data_dict_from_file(data_dict, file):
    print(f"Processing file: {file}")
    try:
        df = pd.read_json(f'github_data/{file}')
        if df.empty:
            return df
        base_row = list(df.base)
        data_dict["Organization Name"] = base_row[0]["user"]["login"]
        data_dict["repository_id"] = base_row[0]["repo"]["id"]
        data_dict["repository_name"] = base_row[0]["repo"]["name"]
        data_dict["repository_owner"] = base_row[0]["repo"]["owner"]["login"]
        data_dict["num_prs"] = df.number.count()
        data_dict["num_prs_merged"] = df[df["merged_at"].notnull()].number.count()
        data_dict["merged_at"] = df["merged_at"].max()
        if (df.number.count() == df[df["merged_at"].notnull()].number.count()) and ("Scytale".lower()) in base_row[0]["repo"]["owner"]["login"].lower():
            data_dict["is_compliant"] = "Compliant"
        else:
            data_dict["is_compliant"] = "Not Compliant"
        final_df = pd.DataFrame(data_dict, index=[0])
        return final_df
    except Exception as e:
        print(f"Error in reading json file: {e}")
        return pd.DataFrame(data_dict)


# Function to transform the data
def transform_data():
    files_list = get_files_in_data_directory()
    return transform_json_files_to_df(files_list).reset_index(drop=True)
