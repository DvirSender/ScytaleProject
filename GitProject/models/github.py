import requests
import json


# function to get all repositories for an organization (Scytale-exercise)
def get_all_repositories(org_name):
    try:
        url = f"https://api.github.com/orgs/{org_name}/repos"
        response = requests.get(url)
        response.raise_for_status()
        repositories = response.json()
        return repositories
    except requests.exceptions.RequestException as err:
        print ("Request Error:",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)

# function to get all pull requests for a repository
def get_all_pull_requests(repo_full_name):
    try:
        url = f"https://api.github.com/repos/{repo_full_name}/pulls"
        params = {"state": "all"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        pull_requests = response.json()
        return pull_requests
    except requests.exceptions.RequestException as err:
        print ("Request Error:",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)

# function to save data to a JSON file
def save_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Error in saving data to json:", e)