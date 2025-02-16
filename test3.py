import subprocess
import log_utils
import zmq
import spec_utils
import udebugfs
import os
import time
import cgroup_utils
import threading
import csv_utils

nproc=1
lazy=0

kernelname=subprocess.getoutput("uname -r")
assert "test3" in kernelname

with open("machinename") as f:
    MachineName=f.read().strip()

context=zmq.Context()

def log(message):
    print(message)
    log_utils.send(context, f"{MachineName}:{message}")
    
DEBUGFS_DIR="/sys/kernel/debug/memory_detector"
DEBUGFS_CONTROL_FILE=f"{DEBUGFS_DIR}/control"
DEBUGFS_INTERVAL_FILE=f"{DEBUGFS_DIR}/scan_interval"
DEBUGFS_LAZY_LEVEL_FILE=f"{DEBUGFS_DIR}/lazy_level"
DEBUGFS_TIME_FILE=f"{DEBUGFS_DIR}/time"
DEBUGFS_COUNT_FILE=f"{DEBUGFS_DIR}/count"
DEBUGFS_READ_FILE=f"{DEBUGFS_DIR}/read"
DEBUGFS_READ_ARRAY_FILE="/dev/memory_detector_history"
CGROUP_ROOT_DIR="/sys/fs/cgroup/memory_detector"
CGROUP_DIR=f"/{CGROUP_ROOT_DIR}/test"
CGROUP_DETECT_FLAG_FILE=f"{CGROUP_DIR}/memory_detector.detect_flag"
CGROUP_TASK_FILE=f"{CGROUP_DIR}/tasks"

def init_scan()->None:
    udebugfs.write_to_debugfs_file(DEBUGFS_CONTROL_FILE,"init")

def clean_scan()->None:
    udebugfs.write_to_debugfs_file(DEBUGFS_CONTROL_FILE,"clean")

def set_interval(interval:int)->None:
    udebugfs.write_to_debugfs_u64(DEBUGFS_INTERVAL_FILE,interval)

def set_lazy_level(level:int)->None:
    udebugfs.write_to_debugfs_u64(DEBUGFS_LAZY_LEVEL_FILE, level)

def get_time()->int:
    return udebugfs.read_from_debugfs_u64(DEBUGFS_TIME_FILE)

def get_count()->int:
    return udebugfs.read_from_debugfs_u64(DEBUGFS_COUNT_FILE)

def set_detect_flag()->None:
    assert os.path.exists(CGROUP_DETECT_FLAG_FILE)
    os.system(f"echo 1 > {CGROUP_DETECT_FLAG_FILE}")


spec_utils.set_path("/root/cpu2006")

results_page_count={}
interval=1000

# define running process

def run_one_time(benchmark:str):
    tmp_data=[]
    log(f"正在测试：{benchmark}")
    spec_utils.setup_one_benchmark(benchmark)
    spec_utils.clean_log()
    init_scan()
    time.sleep(1)
    set_interval(interval)
    cgroup_utils.create_cgroup_dir(CGROUP_DIR)
    set_detect_flag()
    set_lazy_level(lazy)
    spec_utils.run_one_benchmark("test3-runspec.sh",benchmark)
    sum_time=get_time()
    count=get_count()
    avg_time=sum_time/count
    cgroup_utils.delete_cgroup_dir(CGROUP_DIR)
    clean_scan()
    results_page_count[benchmark]=avg_time
    csv_utils.record(f"test3.csv",results_page_count)

for i in range(nproc):
    for benchmark in spec_utils.benchmarklist:
        run_one_time(benchmark)