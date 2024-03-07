import pandas as pd
import os
import json


# # Function to create an empty dictionary with specific keys
# def create_empty_data_dict():
#     data_dict = {
#         "Organization Name": [],
#         "repository_id": [],
#         "repository_name": [],
#         "repository_owner": [],
#         "num_prs": [],
#         "num_prs_merged": [],
#         "merged_at": [],
#         "is_compliant": []
#     }
#     return data_dict


# Function to merge two dataframes
def merge_dataframes(dataframe1, dataframe2):
    merged_df = pd.concat([dataframe1, dataframe2])
    return merged_df


# # Function to transform JSON files into a dataframe
# def transform_json_files_to_df(files_list):
#     result_df = pd.DataFrame(create_empty_data_dict())
#     for file in files_list:
#         if file == []:
#             continue
#         empty_data_dict = create_empty_data_dict()
#         filled_df = fill_data_dict_from_file(empty_data_dict, file)
#         if result_df.empty:
#             result_df = filled_df
#         else:
#             result_df = merge_dataframes(result_df, filled_df)
#     return result_df


# Function to list all files in the data directory
def get_files_in_data_directory(dir_name):
    files_list = os.listdir(dir_name)
    return files_list


# # Function to fill the dictionary with data from the JSON file
# def fill_data_dict_from_file(data_dict, file):
#     print(f"Processing file: {file}")
#     try:
#         df = pd.read_json(f'pull_requests_data/{file}')
#         if df.empty:
#             return df
#         base_row = list(df.base)
#         data_dict["Organization Name"] = base_row[0]["user"]["login"]
#         data_dict["repository_id"] = base_row[0]["repo"]["id"]
#         data_dict["repository_name"] = base_row[0]["repo"]["name"]
#         data_dict["repository_owner"] = base_row[0]["repo"]["owner"]["login"]
#         data_dict["num_prs"] = df.number.count()
#         data_dict["num_prs_merged"] = df[df["merged_at"].notnull()].number.count()
#         data_dict["merged_at"] = df["merged_at"].max()
#         if (df.number.count() == df[df["merged_at"].notnull()].number.count()) and ("Scytale".lower()) in base_row[0]["repo"]["owner"]["login"].lower():
#             data_dict["is_compliant"] = "Compliant"
#         else:
#             data_dict["is_compliant"] = "Not Compliant"
#         final_df = pd.DataFrame(data_dict, index=[0])
#         return final_df
#     except:
#         try:
#             jsonFile = json.load(open("pull_requests_data/SCytale-repo4_pull_requests.json"))
#             dataF = pd.json_normalize(jsonFile)
#             data_dict["Organization Name"] = dataF["name"]
#             data_dict["repository_id"] = dataF["id"]
#             data_dict["repository_name"] = dataF["name"]
#             data_dict["repository_owner"] = dataF["name"]
#             data_dict["num_prs"] = 0
#             data_dict["num_prs_merged"] = 0
#             data_dict["merged_at"] = None
#             data_dict["is_compliant"] = "Compliant"
#             final_df = pd.DataFrame(data_dict, index=[0])

#             return final_df
#         except Exception as e:
#             print(f"Error in reading json file: {e}")
#             return pd.DataFrame(data_dict)
    

def transform_repos_data(repos):
    res_df = pd.DataFrame()
    repo_data = {}
    for repo in repos:
        try:
            with open(f'repositories_data/{repo}') as f:
                json_data = json.load(f)
            df = pd.json_normalize(json_data)
            repo_data["Organization Name"] = df.full_name.values[0].split("/")[0]
            repo_data["repository_id"] = df.id.values[0]
            repo_data["repository_name"] = df.name.values[0]
            repo_data["repository_owner"] = df['owner.login']
            res_df = pd.concat([res_df, pd.DataFrame(repo_data, index=[0])], axis=0, ignore_index=True)
        except Exception as e:
            print(f"Error processing repository {repo}: {e}")
    return res_df

def transform_pr_data(prs):
    res_df = pd.DataFrame()
    pr_data = {}
    for pr in prs:
        try:
            with open(f'pull_requests_data/{pr}') as f:
                json_data = json.load(f)
            df = pd.json_normalize(json_data)
            pr_data["repository_id"] = df['head.repo.id']
            pr_data["num_prs"] = df.number.count()
            pr_data["num_prs_merged"] = df[df["merged_at"].notnull()].number.count()
            pr_data["merged_at"] = df["merged_at"].max()
            res_df = pd.concat([res_df, pd.DataFrame(pr_data, index=[0])], axis=0, ignore_index=True)
        except Exception as e:
            print(f"Error processing pull request {pr}: {e}")
    return res_df


# Function to transform the data
def transform_data():
    repos_name_list = get_files_in_data_directory("repositories_data")
    repos_data = transform_repos_data(repos_name_list)
    pr_files_list = get_files_in_data_directory("pull_requests_data")
    prs_data = transform_pr_data(pr_files_list)
    # print(repos_data)
    # print(prs_data)
    final_df = pd.merge(repos_data, prs_data, on='repository_id', how='left')
    final_df['is_compliant'] = final_df.apply(lambda x: 'Compliant' if x['num_prs'] == x['num_prs_merged'] and "Scytale".lower() in x['repository_owner'].lower() else 'Not Compliant', axis=1)
    return final_df
