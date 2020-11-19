import shutil
import gzip
import requests
import os

def download_file(url, prefix):
    local_filename = prefix + url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f, length=16*1024*1024)

    return local_filename

def gunzip_file(compress_file):
    uncompress_file = compress_file.strip('.gz')
    with gzip.open(compress_file, 'rb') as f_in:
        with open(uncompress_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(compress_file)
    return uncompress_file
