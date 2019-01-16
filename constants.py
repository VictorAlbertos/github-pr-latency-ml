repo_coll = 'repo'
author_coll = 'author'
title_col = 'title'
title_count_col = 'title_count'
body_coll = 'body'
body_count_coll = 'body_count'
created_at_coll = 'created_at'
closed_at_coll = 'closed_at'
pull_requests_neighbours_count_coll = 'pull_requests_neighbours_count'
pull_requests_neighbours_latency_coll = 'pull_requests_neighbours_latency'
latency_coll = 'latency'
reviews_coll = 'reviews'
authors_in_comments_coll = 'authors_in_comments'
diff_file_url_coll = 'diff_file_url'
labels_coll = 'labels'
labels_count_coll = 'labels_count'
commits_coll = 'commits'
commits_count_coll = 'commits_count'
changes_coll = 'changes'
additions_coll = 'additions'
deletions_coll = 'deletions'

cols_pull_request = [repo_coll, 'language', author_coll, title_col, body_coll, created_at_coll, closed_at_coll,
                     authors_in_comments_coll, reviews_coll, labels_coll, additions_coll, deletions_coll, 'changed_files',
                     commits_coll, diff_file_url_coll]

# ('square', 'moshi', 'java'), ('square', 'retrofit', 'java'),('square', 'okhttp', 'java'), ('ReactiveX', 'RxJava', 'java')
# arrow-kt/arrow
repositories = [('twbs', 'bootstrap', 'js'), ('nodejs', 'node', 'js'), ('facebook', 'jest', 'js'),
                ('facebook', 'react', 'js')]

diff_folder = "raw/diff"
raw_data_path = "raw/data.csv"
dataset_path = "dataset.csv"
