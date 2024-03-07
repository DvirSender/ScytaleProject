import pandas as pd
import os
import json


# Function to merge two dataframes
def merge_dataframes(dataframe1, dataframe2):
    merged_df = pd.concat([dataframe1, dataframe2])
    return merged_df


# Function to list all files in the data directory
def get_files_in_data_directory(dir_name):
    files_list = os.listdir(dir_name)
    return files_list

# Function to transform the data of the repositories
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

# Function to transform the data of the pull requests
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
    final_df = pd.merge(repos_data, prs_data, on='repository_id', how='left')
    final_df['is_compliant'] = final_df.apply(lambda x: 'Compliant' if x['num_prs'] == x['num_prs_merged'] and "Scytale".lower() in x['repository_owner'].lower() else 'Not Compliant', axis=1)
    return final_df
