from models.github import git_interact
from models.utils import make_files_directory, save_to_parquet
from models.transform_json import transform_data

if __name__ == "__main__":
    make_files_directory("github_data")
    git_interact("Scytale-exercise")
    df = transform_data()
    make_files_directory("parquet_data")
    save_to_parquet(df, "parquet_data/github_pull_requests.parquet")
