import os

def mount_cgroup_root_dir(CGROUP_ROOT_DIR_PATH:str, CGROUP_SYS_NAME:str):
    if not os.path.exists(CGROUP_ROOT_DIR_PATH):
        os.system(f"mkdir {CGROUP_ROOT_DIR_PATH}")
    os.system(f"mount -t cgroup -o {CGROUP_SYS_NAME} {CGROUP_SYS_NAME} {CGROUP_ROOT_DIR_PATH}")

def create_cgroup_dir(CGROUP_DIR:str)->None:
    if not os.path.exists(CGROUP_DIR):
        os.system(f"mkdir {CGROUP_DIR}")
    assert os.path.exists(f"{CGROUP_DIR}/tasks")

def delete_cgroup_dir(CGROUP_DIR:str)->None:
    assert os.path.exists(f"{CGROUP_DIR}/tasks")
    os.system(f"rmdir {CGROUP_DIR}")
    assert not os.path.exists(f"{CGROUP_DIR}/tasks")