from github import Github
import pandas as pd

USER_NAME = "Scytale-exercise"


def get_pull_requests(dict_of_repos, user, git_object):
    for item in dict_of_repos:
        print()
        repo = git_object.get_repo(f"{USER_NAME}/{dict_of_repos[item]['repo_name']}")
        pulls = repo.get_pulls(state='closed')
        for pull in pulls:
            dict_of_repos[item]['repo_pull_requests'].append(pull)
    print(dict_of_repos)


def get_the_repos_pull_requests():
    repository_dict = {}
    git_object = Github()
    git_user_to_interact = git_object.get_user(USER_NAME)
    repos = git_user_to_interact.get_repos()
    list_of_repos_names = []
    for index, repo in enumerate(repos):
        list_of_repos_names.append(repo.name)
        key_string = f"repository-{index}"
        repository_dict[key_string] = {"repo_name": repo.name,
                                    "repo_pull_requests": []
                                  }
    get_pull_requests(repository_dict, git_user_to_interact, git_object)
    df = pd.DataFrame(list_of_repos_names, columns=['repo_name'])
    df['org_name'] = USER_NAME
    print(df.to_json('text.json'))