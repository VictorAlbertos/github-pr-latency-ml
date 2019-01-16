import pandas as pd
import numpy as np
import ast
from constants import raw_data_path, author_coll, body_coll, created_at_coll, closed_at_coll, latency_coll, \
    reviews_coll, authors_in_comments_coll, labels_coll, repo_coll, pull_requests_neighbours_latency_coll, \
    pull_requests_neighbours_count_coll, dataset_path, title_col, title_count_col, body_count_coll, labels_count_coll, \
    commits_coll, commits_count_coll, changes_coll, additions_coll, deletions_coll

days_back_mean_latency = 14


def map_strings_columns_to_list(df):
    df[authors_in_comments_coll] = df[authors_in_comments_coll].apply(ast.literal_eval)
    df[labels_coll] = df[labels_coll].apply(ast.literal_eval)
    df[reviews_coll] = df[reviews_coll].apply(ast.literal_eval)
    df[commits_coll] = df[commits_coll].apply(ast.literal_eval)


def add_count_to_target_string_columns(df):
    df[title_count_col] = df[title_col].str.len()
    df[body_count_coll] = df[body_coll].str.len()


def add_count_to_target_list_columns(df):
    df[labels_count_coll] = df[labels_coll].apply(lambda x: len(x))
    df[commits_count_coll] = df[commits_coll].apply(lambda x: len(x))

    for index, row in df.iterrows():
        df.loc[index, labels_count_coll] = len(row[labels_coll])
        df.loc[index, commits_count_coll] = len(row[commits_coll])


def impute_nan_values(df):
    df[[body_coll, author_coll]] = df[[body_coll, author_coll]].fillna(value='')

    if df.isnull().sum().sum() != 0:
        raise ValueError('There are still nan values')


def evaluate_latency(created_at, closed_at):
    return int(round(pd.Timedelta(closed_at - created_at).seconds / 60.0))


def convert_dates_to_latency_in_minutes(df):
    df[created_at_coll] = pd.to_datetime(df[created_at_coll])
    df[closed_at_coll] = pd.to_datetime(df[closed_at_coll])
    df[latency_coll] = np.vectorize(evaluate_latency)(df[created_at_coll], df[closed_at_coll])


def calculate_mean_latency_and_occurrences_nearest_pull_requests(df):
    for index, row in df.iterrows():
        repo_name = row[repo_coll]

        created_target_date = row[created_at_coll] - pd.Timedelta(f'{days_back_mean_latency} day')
        closed_target_date = row[created_at_coll] - pd.Timedelta(f'1 day')

        df_filtered = df[(df[created_at_coll] >= created_target_date) & (df[closed_at_coll] <= closed_target_date)
                         & (df[repo_coll] == repo_name)]

        df.loc[index, pull_requests_neighbours_latency_coll] = int(df_filtered[latency_coll].sum())
        df.loc[index, pull_requests_neighbours_count_coll] = int(df_filtered.shape[0])

    df[pull_requests_neighbours_latency_coll] = df[pull_requests_neighbours_latency_coll].astype(int)
    df[pull_requests_neighbours_count_coll] = df[pull_requests_neighbours_count_coll].astype(int)


def filter_pull_request_no_reviewed(row):
    authors_in_comments = [author for author in row[authors_in_comments_coll] if not row[author_coll] in author]
    return 'APPROVED' in row[reviews_coll] or len(authors_in_comments) != 0


def add_changes_count_column(df):
    def changes_count(additions, deletions):
        return additions + deletions

    df[changes_coll] = np.vectorize(changes_count)(df[additions_coll], df[deletions_coll])


df = pd.read_csv(raw_data_path)

map_strings_columns_to_list(df)

impute_nan_values(df)

add_changes_count_column(df)

add_count_to_target_string_columns(df)

add_count_to_target_list_columns(df)

df = df[df.apply(filter_pull_request_no_reviewed, axis=1)]

convert_dates_to_latency_in_minutes(df)

calculate_mean_latency_and_occurrences_nearest_pull_requests(df)

df = df[df[pull_requests_neighbours_count_coll] > days_back_mean_latency / 7]

df.to_csv(dataset_path, index=False)
