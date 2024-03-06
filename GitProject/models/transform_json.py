import pandas as pd
import os


def create_empty_dictionary():
    data = {"Organization Name": [], "repository_id": [], "repository_name": [], "repository_owner": [], "num_prs": [], "num_prs_merged": [], "merged_at": [], "is_compliant": []}
    return data


def merge_datafranes(data, filled_df):
    df = pd.concat([data, filled_df])
    return df


def transform_json_files(files_list):
    res_df = pd.DataFrame(create_empty_dictionary())
    for file in files_list:
        if file == []:
            pass
        empty_dictionary = create_empty_dictionary()
        filled_df = fill_dictionary(empty_dictionary, file)
        if res_df.empty:
            res_df = filled_df
        else:
            res_df = merge_datafranes(res_df, filled_df)
    return res_df


def list_files_in_data_directory():
    files_list = os.listdir("github_data")
    return files_list


def fill_dictionary(data, file):
    df = pd.read_json(f'github_data/{file}')
    if df.base:
        try:
            
            if df.empty:
                return df
            base_row = list(df.base)
            data["repository_id"] = base_row[0]["repo"]["id"]
            data["Organization Name"] = base_row[0]["user"]["login"]
            data["repository_name"] = base_row[0]["repo"]["name"]
            data["repository_owner"] = base_row[0]["repo"]["owner"]["login"]
            data["num_prs"] = df.number.count()
            data["num_prs_merged"] = df[df["merged_at"].notnull()].number.count()
            data["merged_at"] = df["merged_at"].max()
            if (df.number.count() == df[df["merged_at"].notnull()].number.count()) and ("Scytale".lower()) in base_row[0]["repo"]["owner"]["login"].lower():
                data["is_compliant"] = "Compliant"
            else:
                data["is_compliant"] = "Not Compliant"
            final_df = pd.DataFrame(data, index=[0])
            return final_df
        except Exception as e:
            print("Error in reading json file:", e)
    else:
        return pd.DataFrame(create_empty_dictionary(), index=[0])


def transform_data():
    files_list = list_files_in_data_directory()
    return (transform_json_files(files_list).reset_index(drop=True))
