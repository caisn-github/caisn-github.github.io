from __future__ import absolute_import
import spec_utils
import scan_utils
import time
import pandas as pd
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
assert "motivation2" in kernelname

with open("machinename") as f:
    MachineName=f.read().strip()

def log(message):
    print(message)

DEBUGFS_DIR="/sys/kernel/debug/memory_detector"
DEBUGFS_PID_FILE=f"{DEBUGFS_DIR}/pid"
DEBUGFS_TRIGGER_SCAN_FILE=f"{DEBUGFS_DIR}/trigger_scan"
DEBUGFS_RSS_COUNT_FILE=f"{DEBUGFS_DIR}/rss_count"

# define debugfs operations
def trigger_scan():
    udebugfs.write_to_debugfs_u64(DEBUGFS_TRIGGER_SCAN_FILE,1)

def get_rss_count():
    return udebugfs.read_from_debugfs_u64(DEBUGFS_RSS_COUNT_FILE)

spec_utils.set_path("/root/cpu2006")

results_rss_count={}
interval=1000

# define recording thread
recording_thread_stop_event = threading.Event()
def test_recording_thread(benchmark:str,data:list,interval:int, recording_thread_stop_event):
    while not recording_thread_stop_event.is_set():
        trigger_scan()
        rss_count=get_rss_count()
        print(f"{benchmark}:{rss_count}")
        data.append(rss_count)
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
    start_recording_thread(test_recording_thread,benchmark,tmp_data,interval)
    spec_utils.run_one_benchmark("motivation2-runspec.sh",benchmark)
    end_recording_thread()
    results_rss_count[benchmark]=tmp_data
    csv_utils.record(f"motivation2.csv",results_rss_count)

for i in range(nproc):
    for benchmark in spec_utils.benchmarklist:
        run_one_time(benchmark)
        