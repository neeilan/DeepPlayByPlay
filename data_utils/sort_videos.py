from os import listdir
from os import mkdir
from os import path
from shutil import copy2

UNSORTED_VIDS_DIR = '/path/to/dir/containing/unsorted/video/files'     # ex - '/Users/username/Desktop/all_videos'
DEST_DIR = '/path/where/you/want/sorted/folders/to/go'                 # ex - '/Users/username/Desktop/sorted_videos'

THREE_POINT_MAKE = 'THREE_POINT_MAKE'
THREE_POINT_MISS = 'THREE_POINT_MISS'
MIDRANGE_MAKE = 'MIDRANGE_MAKE'
MIDRANGE_MISS = 'MIDRANGE_MISS'
INSIDE_MAKE = 'INSIDE_MAKE'
INSIDE_MISS = 'INSIDE_MISS'


def _get_class(name):
    miss = 'MISS' in name
    if '3PT' in name:
        return THREE_POINT_MISS if miss else THREE_POINT_MAKE
    if any(keyword in name for keyword in ['LAYUP', 'DUNK', 'DRIVING', 'HOOK']):
        return INSIDE_MISS if miss else INSIDE_MAKE
    return MIDRANGE_MISS if miss else MIDRANGE_MAKE


def init_class_dirs(class_dirs_root):
    for class_name in [
        THREE_POINT_MAKE,
        THREE_POINT_MISS,
        MIDRANGE_MAKE,
        MIDRANGE_MISS,
        INSIDE_MAKE,
        INSIDE_MISS]:
                class_dir_path = path.join(class_dirs_root, class_name)
                if not path.isdir(class_dir_path):
                    mkdir(class_dir_path)

        
def sort_files(src_dir, class_dirs_root):
    for file_name in listdir(src_dir):
        class_name = _get_class(file_name)

        class_dir_path = path.join(class_dirs_root, class_name)
        file_path = path.join(src_dir, file_name)
        copy2(file_path, class_dir_path)

if __name__ == '__main__':
    src_dir = UNSORTED_VIDS_DIR
    dest_dir = DEST_DIR

    init_class_dirs(dest_dir)
    sort_files(src_dir, dest_dir)
