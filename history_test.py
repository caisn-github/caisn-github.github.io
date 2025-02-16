from __future__ import absolute_import
import spec_utils
import time
import subprocess
import udebugfs
import os
import threading
import cgroup_utils

nproc=1
lazy=0

with open("machinename") as f:
    MachineName=f.read().strip()

def log(message):
    print(message)

DEBUGFS_DIR="/sys/kernel/debug/repabp"
DEBUGFS_CONTROL_FILE=f"{DEBUGFS_DIR}/control"
DEBUGFS_INTERVAL_FILE=f"{DEBUGFS_DIR}/scan_interval"
DEBUGFS_READ_HISTORY_FILE=f"{DEBUGFS_DIR}/read_history"
DEBUGFS_MAX_PFN_FILE=f"{DEBUGFS_DIR}/max_pfn"

CGROUP_ROOT_DIR="/repabp"
CGROUP_DIR=f"{CGROUP_ROOT_DIR}/test"
CGROUP_DETECT_FLAG_FILE=f"{CGROUP_DIR}/repabp.detect_flag"
CGROUP_TASK_FILE=f"{CGROUP_DIR}/tasks"

def init_scan()->None:
    udebugfs.write_to_debugfs_file(DEBUGFS_CONTROL_FILE,"init")

def clean_scan()->None:
    udebugfs.write_to_debugfs_file(DEBUGFS_CONTROL_FILE,"clean")

def set_scan_interval(interval:int)->None:
    udebugfs.write_to_debugfs_u64(DEBUGFS_INTERVAL_FILE,interval)

def set_detect_flag()->None:
    assert os.path.exists(CGROUP_DETECT_FLAG_FILE)
    os.system(f"echo 1 > {CGROUP_DETECT_FLAG_FILE}")

def record_thread():
    subprocess.getoutput("./record")

def start_recording()->None:
    os.system("echo 1 > ./runflag")
    t=threading.Thread(target=record_thread)
    t.start()

def end_recording(benchmark:str)->None:
    os.system("echo 0 > ./runflag")
    while "0" not in subprocess.getoutput("cat ./record_lock"):
        time.sleep(0.1)
    os.system(f"cp history {benchmark}.history")

spec_utils.set_path("/root/cpu2006")

interval=1000

def run_one_time(benchmark:str):
    log(f"正在测试：{benchmark}")
    spec_utils.setup_one_benchmark(benchmark)
    spec_utils.clean_log()
    set_scan_interval(interval)
    init_scan()
    time.sleep(1)
    cgroup_utils.mount_cgroup_root_dir(CGROUP_ROOT_DIR,"repabp")
    cgroup_utils.create_cgroup_dir(CGROUP_DIR)
    set_detect_flag()
    start_recording()
    spec_utils.run_one_benchmark("history_test-runspec.sh",benchmark)
    end_recording(benchmark)
    cgroup_utils.delete_cgroup_dir(CGROUP_DIR)
    clean_scan()
    spec_utils.clean_one_benchmark(benchmark)

for i in range(nproc):
    for benchmark in spec_utils.benchmarklist:
        run_one_time(benchmark)
