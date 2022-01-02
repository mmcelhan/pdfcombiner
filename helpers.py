import os


def initialize():
    # initializes program by ensuring that download folder is created
    cur_work_dir = os.getcwd()
    dl_path = os.path.join(cur_work_dir, 'downloads')
    make_dir_if_not_exists(dl_path)
    return None

def make_dir_if_not_exists(path):
    # makes directory if it doesn't exist
    os.makedirs(path, exist_ok=True)
    return None