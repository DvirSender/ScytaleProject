from models.github import get_the_repos_pull_requests


def main():
    repos_dict = get_the_repos_pull_requests()

if __name__ == "__main__":
    main()
