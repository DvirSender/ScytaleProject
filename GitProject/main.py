from models.github import interact_with_github_api
from models.utils import create_directory_if_not_exists, save_dataframe_to_parquet_file
from models.transform_json import transform_data

if __name__ == "__main__":
    # Create a directory to store GitHub data
    create_directory_if_not_exists("pull_requests_data")

    # Interact with GitHub API and fetch data for the organization "Scytale-exercise"
    interact_with_github_api("Scytale-exercise")

    # Transform the fetched data
    transformed_data = transform_data()

    # Print the transformed data
    print(transformed_data)

    # Create a directory to store the transformed data in parquet format
    create_directory_if_not_exists("parquet_data")

    # Save the transformed data to a parquet file
    save_dataframe_to_parquet_file(transformed_data, "parquet_data/github_pull_requests.parquet")
