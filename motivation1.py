from __future__ import absolute_import
import spec_utils
import scan_utils
import time
import pandas as pd
import zmq
import sys
import subprocess
import log_utils
import csv_utils
import udebugfs
import cgroup_utils
import os
import threading

nproc=1
kernelname=subprocess.getoutput("uname -r")
assert "motivation1" in kernelname

with open("machinename") as f:
    MachineName=f.read().strip()

context=zmq.Context()

def log(message):
    print(message)
    log_utils.send(context, f"{MachineName}:{message}")

DEBUGFS_DIR="/sys/kernel/debug/memory_detector"
DEBUGFS_CONTROL_FILE=f"{DEBUGFS_DIR}/control"
DEBUGFS_ALLOCATION_COUNT_FILE=f"{DEBUGFS_DIR}/allocation_count"
CGROUP_ROOT_DIR="/sys/fs/cgroup/memory_detector"
CGROUP_DIR=f"/{CGROUP_ROOT_DIR}/test"
CGROUP_DETECT_FLAG_FILE=f"{CGROUP_DIR}/memory_detector.detect_flag"
CGROUP_TASK_FILE=f"{CGROUP_DIR}/tasks"

# define debugfs operations
def init_allocation_count():
    udebugfs.write_to_debugfs_u64(DEBUGFS_ALLOCATION_COUNT_FILE,0)

def get_allocation_count():
    return udebugfs.read_from_debugfs_u64(DEBUGFS_ALLOCATION_COUNT_FILE)

def set_detect_flag():
    assert os.path.exists(CGROUP_DETECT_FLAG_FILE)
    os.system(f"echo 1 > {CGROUP_DETECT_FLAG_FILE}")

spec_utils.set_path("/root/cpu2006")

results_page_alloc_count={}
interval=1000

# define recording thread
recording_thread_stop_event = threading.Event()
def test_recording_thread(benchmark:str,data:list,interval:int, recording_thread_stop_event):
    while not recording_thread_stop_event.is_set():
        allocation_count=get_allocation_count()
        print(f"{benchmark}:{allocation_count}")
        init_allocation_count()
        data.append(allocation_count)
        time.sleep(1)

def start_recording_thread(recording_thread, benchmark:str,data,interval:int)->None:
    global recording_thread_stop_event
    
    # recording_thread_stop_event= threading.Event()
    recording_thread_stop_event.clear()
    t=threading.Thread(target=test_recording_thread,args=(benchmark,data,interval,recording_thread_stop_event))
    t.start()

def end_recording_thread()->None:
    global recording_thread_stop_event
    
    recording_thread_stop_event.set()
    time.sleep(3)

# define running process

def run_one_time(benchmark:str):
    tmp_data=[]
    log(f"正在测试：{benchmark}")
    spec_utils.setup_one_benchmark(benchmark)
    spec_utils.clean_log()
    init_allocation_count()
    cgroup_utils.create_cgroup_dir(CGROUP_DIR)
    set_detect_flag()
    start_recording_thread(test_recording_thread,benchmark,tmp_data,interval)
    spec_utils.run_one_benchmark("motivation1-runspec.sh",benchmark)
    end_recording_thread()
    cgroup_utils.delete_cgroup_dir(CGROUP_DIR)
    results_page_alloc_count[benchmark]=tmp_data
    csv_utils.record(f"motivation1.csv",results_page_alloc_count)

for i in range(nproc):
    for benchmark in spec_utils.benchmarklist:
        run_one_time(benchmark)

# if not test_flag:
#     for benchmark in spec_utils.benchmarklist:
#         statistic, p_value = normaltest(results[benchmark])
#         alpha = 0.05
#         if p_value >= alpha:
#             break
#         else:
#             log(f"{benchmark}不符合正态分布")
