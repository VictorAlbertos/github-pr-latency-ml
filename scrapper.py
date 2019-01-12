from github import Github
import pandas as pd
from constants import cols_pull_request, repos_names, raw_data_path, diff_folder
from credentials import token
import urllib.request
from urllib.parse import urlparse

df = pd.DataFrame(columns=[cols_pull_request])

g = Github(token)


def save_diff_file(diff_url):
    diff = urllib.request.urlopen(diff_url).read()
    diff_file_name = urlparse(pull.diff_url).path.replace("/", "_")[1:]
    diff_path = f'{diff_folder}/{diff_file_name}.txt'

    text_file = open(diff_path, "wb")
    text_file.write(diff)
    text_file.close()

    return diff_file_name


for repo_name in repos_names:
    pull_requests = g.get_repo(repo_name).get_pulls('closed')

    print(f"Fetching {pull_requests.totalCount} PRs from {repo_name}")

    for index, pull in enumerate(pull_requests):
        diff_file_name = save_diff_file(pull.diff_url)

        labels = [label.name for label in pull.labels]
        df.loc[len(df)] = [repo_name, pull.title, pull.body, pull.created_at, pull.closed_at, pull.issue_url,
                           labels, pull.additions, pull.deletions, diff_file_name]

        print(f"PRs #{index} fetched")

df.to_csv(raw_data_path, index=False)
