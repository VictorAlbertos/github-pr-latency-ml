repo_coll = 'repo'
diff_file_url = 'diff_file_url'

cols_pull_request = [repo_coll, 'language', 'author', 'title', 'body', 'created_at', 'closed_at',
                     'authors_in_comments', 'reviews', 'labels', 'additions', 'deletions', 'changed_files',
                     'commits', 'diff_file_url']

# ('square', 'moshi', 'java'), ('square', 'retrofit', 'java'),('square', 'okhttp', 'java'), ('ReactiveX', 'RxJava', 'java')
# arrow-kt/arrow
repositories = [('twbs', 'bootstrap', 'js'), ('nodejs', 'node', 'js'), ('facebook', 'jest', 'js'),
                ('facebook', 'react', 'js')]

diff_folder = "raw/diff"
raw_data_path = "raw/data.csv"
