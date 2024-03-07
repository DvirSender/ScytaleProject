import os
import json


# Function to create a directory if it doesn't exist
def create_directory_if_not_exists(directory_name):
    os.makedirs(directory_name, exist_ok=True)


# Function to save data to a JSON file
def save_data_to_json_file(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as error:
        print("Error in saving data to json:", error)


# Function to save a DataFrame to a Parquet file
def save_dataframe_to_parquet_file(dataframe, filename):
    try:
        dataframe.to_parquet(filename)
    except Exception as error:
        print("Error in saving data to parquet:", error)
