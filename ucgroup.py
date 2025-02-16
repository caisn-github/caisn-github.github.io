import os

def create_cgroup_dir(path:str)->None:
    if not os.path.exists(path):
        os.system(f"mkdir {path}")
    assert os.path.exists(path)