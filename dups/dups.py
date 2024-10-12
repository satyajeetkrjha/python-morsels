from collections import defaultdict
from io import DEFAULT_BUFFER_SIZE
import hashlib
from pathlib import Path
from argparse import ArgumentParser

#this returns the hash of the file
def hash_file(filename):
    md5 = hashlib.md5()
    with open(filename, mode='rb') as f:
        for chunk in iter(lambda: f.read(DEFAULT_BUFFER_SIZE), b''):
            md5.update(chunk)
    return md5.hexdigest()

# returns a list of files by walking into directory ,subdirectory 
def walk(path):
    if path.is_file():
        return [path]
    return (item for item in path.rglob('*') if item.is_file())

#returns a set of files by splitting them on basis of comma operator and removes duplicates and finally returns a set
def file_list(delimited_filenames):
    return set(delimited_filenames.split(','))


def find_duplicates(filenames,min_size =0, ignores = frozenset()):
    groups = defaultdict(list)
    for filename in filenames:
        for path in walk(Path(filename)):
            if path.stat().st_size < min_size or (ignores & set(path.parts)):
                continue
            hash_value = hash_file(path)
            groups[hash_value].append(path)
    return {
        frozenset(group) for group in groups.values() if len (group) > 1
    }        
            
                
            

def main(args):
    duplicate_groups = find_duplicates(args.filenames, args.min_size,args.ignore)
    index = None
    for index ,group in enumerate(duplicate_groups,start =1):
        print(f"Duplicate group {index}:")
        for filename in sorted(group):
            print(filename)
    
    if not index:
        print("No duplicate files found")
                
    

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('filenames',nargs='+')
    parser.add_argument('--min-size',type=int,default=0)
    parser.add_argument('--ignore',type=file_list,default= set())
    args = parser.parse_args()
    main(args)
    
    
    
            