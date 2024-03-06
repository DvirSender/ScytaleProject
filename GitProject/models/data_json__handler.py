import pandas as pd

df = pd.read_json('github_data/scytale-repo3_pull_requests.json')
print(df.columns)