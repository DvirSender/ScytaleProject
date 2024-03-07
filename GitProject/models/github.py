import requests
from models.utils import save_data_to_json_file, create_directory_if_not_exists


# Function to fetch all repositories for a given organization
def fetch_all_repositories(organization_name):
    try:
        api_url = f"https://api.github.com/orgs/{organization_name}/repos"
        api_response = requests.get(api_url)
        api_response.raise_for_status()
        repositories = api_response.json()
        return repositories
    except requests.exceptions.RequestException as request_error:
        print("Request Error:", request_error)
    except requests.exceptions.HTTPError as http_error:
        print("Http Error:", http_error)
    except requests.exceptions.ConnectionError as connection_error:
        print("Error Connecting:", connection_error)
    except requests.exceptions.Timeout as timeout_error:
        print("Timeout Error:", timeout_error)





# Function to fetch all pull requests for a given repository
def fetch_all_pull_requests(repository_full_name):
    try:
        api_url = f"https://api.github.com/repos/{repository_full_name}/pulls"
        api_params = {"state": "all"}
        api_response = requests.get(api_url, params=api_params)
        api_response.raise_for_status()
        pull_requests = api_response.json()
        return pull_requests
    except requests.exceptions.RequestException as request_error:
        print("Request Error:", request_error)
    except requests.exceptions.HTTPError as http_error:
        print("Http Error:", http_error)
    except requests.exceptions.ConnectionError as connection_error:
        print("Error Connecting:", connection_error)
    except requests.exceptions.Timeout as timeout_error:
        print("Timeout Error:", timeout_error)


# Function to interact with GitHub API and save the data
def interact_with_github_api(organization_name="Scytale-exercise"):
    repositories = fetch_all_repositories(organization_name)
    create_directory_if_not_exists("repositories_data")
    for repo in repositories:
        save_data_to_json_file(repo, f"repositories_data/{repo['name']}.json")
    for repo in repositories:
        if repo != []:
            repository_full_name = repo["full_name"]
            pull_requests = fetch_all_pull_requests(repository_full_name)
            # Save pull requests data to a JSON file
            save_data_to_json_file(pull_requests, f"pull_requests_data/{repo['name']}_pull_requests.json")
