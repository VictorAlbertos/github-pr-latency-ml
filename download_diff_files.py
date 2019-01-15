import urllib.request
from constants import diff_folder, diff_file_url
from urllib.parse import urlparse
import pandas as pd
from constants import raw_data_path
from pathlib import Path


def diff_path(diff_url):
    diff_file_name = urlparse(diff_url).path.replace("/", "_")[1:]
    return f'{diff_folder}/{diff_file_name}.txt'


def download_diff_file(diff_url):
    diff = urllib.request.urlopen(diff_url).read()
    text_file = open(diff_path(diff_url), "wb")
    text_file.write(diff)
    text_file.close()


df = pd.read_csv(raw_data_path)
urls_files_to_download = []

for index, row in df.iterrows():
    diff_url = row[diff_file_url]
    file = Path(diff_path(diff_url))
    if file.is_file():
        continue
    else:
        urls_files_to_download.append(row[diff_file_url])

print(f'{len(urls_files_to_download)} files to download')

for index, url_file in enumerate(urls_files_to_download):
    print(f'Downloading {index} file with url: {url_file}')
    download_diff_file(url_file)

