import os

from models.github import get_all_repositories, get_all_pull_requests, save_to_json

if __name__ == "__main__":
    
    
    # Replace 'your_organization_name' with your actual organization name
    organization_name = "Scytale-exercise"
    
    # Create a directory to store the JSON files
    os.makedirs("github_data", exist_ok=True)
    
    # Get all repositories for the organization
    repositories = get_all_repositories(organization_name)
    
    for repo in repositories:
        # Get pull requests for each repository
        repo_full_name = repo["full_name"]
        pull_requests = get_all_pull_requests(repo_full_name)
        
        # Save pull requests data to a JSON file
        save_to_json(pull_requests, f"github_data/{repo['name']}_pull_requests.json")
        
        print(f"Pull requests for {repo['name']} saved to {repo['name']}_pull_requests.json")
