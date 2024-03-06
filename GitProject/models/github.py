import requests
from models.utils import save_to_json
# function to get all repositories for an organization (Scytale-exercise)
def get_all_repositories(org_name):
    try:
        url = f"https://api.github.com/orgs/{org_name}/repos"
        response = requests.get(url)
        response.raise_for_status()
        repositories = response.json()
        return repositories
    except requests.exceptions.RequestException as err:
        print("Request Error:", err)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)


# function to get all pull requests for a repository
def get_all_pull_requests(repo_full_name):
    try:
        url = f"https://api.github.com/repos/{repo_full_name}/pulls"
        params = {"state": "all"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        pull_requests = response.json()
        if pull_requests == []:
            url = f"https://api.github.com/repos/{repo_full_name}"
            response = requests.get(url)
            response.raise_for_status()
            pull_requests = response.json()
        return pull_requests
    except requests.exceptions.RequestException as err:
        print("Request Error:", err)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)


def git_interact(organization_name="Scytale-exercise"):
    repositories = get_all_repositories(organization_name)
    for repo in repositories:
        # Get pull requests for each repository
        repo_full_name = repo["full_name"]
        pull_requests = get_all_pull_requests(repo_full_name)
        # Save pull requests data to a JSON file
        save_to_json(pull_requests, f"github_data/{repo['name']}_pull_requests.json", repo)