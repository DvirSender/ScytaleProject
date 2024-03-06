import pandas as pd
import os


def create_empty_dictionary():
    data = {"org_name": [], "repo_id": [], "repo_name": [], "repo_owner": [], "number_of_prs": [], "number_of_merge_prs": [], "last_merge_pr": [], "is_compliant": []}
    return data


def merge_datafranes(data, filled_df):
    df = pd.concat([data, filled_df])
    return df


def read_json_files(files_list):
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
    print(res_df)
    return res_df


def list_files_in_data_directory():
    files_list = os.listdir("github_data")
    return files_list


def fill_dictionary(data, file):
    try:
        df = pd.read_json(f'github_data/{file}')
        if df.empty:
            return df
        base_row = list(df.base)
        data["repo_id"] = base_row[0]["repo"]["id"]
        data["org_name"] = base_row[0]["user"]["login"]
        data["repo_name"] = base_row[0]["repo"]["name"]
        data["repo_owner"] = base_row[0]["repo"]["owner"]["login"]
        data["number_of_prs"] = df.number.count()
        data["number_of_merge_prs"] = df[df["merged_at"].notnull()].number.count()
        data["last_merge_pr"] = df["merged_at"].max()
        if (df.number.count() == df[df["merged_at"].notnull()].number.count()) and ("Scytale") in base_row[0]["repo"]["owner"]["login"]:
            data["is_compliant"] = "Compliant"
        else:
            data["is_compliant"] = "Not Compliant"
        final_df = pd.DataFrame(data, index=[0])
        return final_df
    except Exception as e:
        print("Error in reading json file:", e)

    
def transform_data():
    files_list = list_files_in_data_directory()
    read_json_files(files_list)


transform_data()