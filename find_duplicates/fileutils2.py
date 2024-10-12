
from collections import defaultdict
from io import DEFAULT_BUFFER_SIZE
import hashlib
from pathlib import Path


#this returns the hash of the file
def hash_file(file_obj):
    md5 = hashlib.md5()
    for chunk in iter(lambda: file_obj.read(DEFAULT_BUFFER_SIZE),b''):
        md5.update(chunk)
    return md5.hexdigest()

#this returns files of similar size
def files_of_same_size(filenames):
    files_by_size = defaultdict(list)
    for filename in filenames:
        files_by_size[Path(filename).stat().st_size].append(filename)
    return (name for group in files_by_size.values() for name in group if len(group)>1)
        

def find_duplicates(filenames):
    files_by_hash = defaultdict(list)
    for filename in files_of_same_size(filenames):
        with open(filename,mode='rb') as f:
            files_by_hash[hash_file(f)].append(filename)
    return {frozenset(group) for group in files_by_hash.values() if len(group)>1}        

