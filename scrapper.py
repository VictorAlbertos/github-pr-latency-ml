import pandas as pd
from constants import cols_pull_request, repositories, raw_data_path
from credentials import token

import requests
import time


def build_pull_request_payload(repo_owner, repo_name, cursor):
    query = """
            query($repo_owner:String!, $repo_name:String!, $cursor:String) {
                repository(owner:$repo_owner, name:$repo_name) {
                pullRequests(first: 100, states:MERGED, after:$cursor) {
                  totalCount
                  pageInfo {
                      hasNextPage
                      endCursor
                  }
                  edges {
                    node {
                      author {
                        login
                      }
                      number
                      title
                      body
                      changedFiles
                      createdAt
                      closedAt
                      comments(last:10) {
                        nodes {
                          author {
                            login
                          }
                        }
                      }
                      reviews(last:10) {
                        nodes {
                          state
                        }
                      }
                      labels(last:10) {
                        nodes {
                          name
                        }
                      }
                      additions
                      deletions
                      changedFiles
                      commits(last:50) {
                        nodes {
                          commit {
                            message
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            """

    variables = {
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "cursor": cursor
    }

    return (query, variables)


def make_http_call(query, variables, retry=0):
    try:
        time.sleep(5)
        request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables},
                                headers={"Authorization": f"Bearer {token}"}, timeout=10)
    except requests.exceptions.Timeout:
        print(f"Retrying http call times {retry}")
        return make_http_call(query, variables, retry + 1)

    if request.status_code == 200:
        return request.json()
    if request.status_code == 502 and retry < 5:
        print("Retrying http call")
        return make_http_call(query, variables, retry + 1)
    else:
        raise Exception(
            "Query failed to run by returning code of {}. Error message: {}. Query: {}".format(request.status_code,
                                                                                               request.content, query))





try:
    df = pd.read_csv(raw_data_path)
except IOError as e:
    df = pd.DataFrame(columns=[cols_pull_request])

for repo_owner, repo_name, repo_language in repositories:
    has_next_page = True
    cursor = None

    page = 1

    while has_next_page:
        (query, variables) = build_pull_request_payload(repo_owner, repo_name, cursor)
        response = make_http_call(query, variables)

        response = response['data']['repository']['pullRequests']

        print(f"Fetching {page}/{int(response['totalCount'] / 100)} PRs from {repo_owner}/{repo_name}")

        has_next_page = response['pageInfo']['hasNextPage']
        cursor = response['pageInfo']['endCursor']

        for edge in response['edges']:
            node = edge['node']

            author = node['author']
            if author is not None:
                author = author['login']

            labels = [node['name'] for node in node['labels']['nodes']]
            commits = [node['commit']['message'] for node in node['commits']['nodes']]
            reviews = [node['state'] for node in node['reviews']['nodes']]
            authors_in_comments = [node['author']['login'] for node in node['comments']['nodes'] if node['author'] is not None]


            number = node['number']
            diff_file_url = f'https://github.com/{repo_owner}/{repo_name}/pull/{number}.diff'

            df.loc[len(df)] = [repo_name, repo_language, author, node['title'], node['body'],
                               node['createdAt'], node['closedAt'], authors_in_comments,
                               reviews, labels, node['additions'], node['deletions'], node['changedFiles'], commits,
                               diff_file_url]

        page += 1

        df.to_csv(raw_data_path, index=False)
