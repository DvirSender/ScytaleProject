import os
import json

def make_files_directory(dir_name):
    os.makedirs(dir_name, exist_ok=True)


# function to save data to a JSON file
def save_to_json(data, filename, repo):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Pull requests for {repo['name']} saved to {repo['name']}_pull_requests.json")
    except Exception as e:
        print("Error in saving data to json:", e)


def save_to_parquet(data, filename):
    try:
        data.to_parquet(filename)
        print(f"Data saved to {filename}")
    except Exception as e:
        print("Error in saving data to parquet:", e)