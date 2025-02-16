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
assert "test2" in kernelname

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
DEBUGFS_PAGE_COUNT_FILE=f"{DEBUGFS_DIR}/page_count"
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

def get_page_count()->int:
    return udebugfs.read_from_debugfs_u64(DEBUGFS_PAGE_COUNT_FILE)

def set_detect_flag()->None:
    assert os.path.exists(CGROUP_DETECT_FLAG_FILE)
    os.system(f"echo 1 > {CGROUP_DETECT_FLAG_FILE}")


spec_utils.set_path("/root/cpu2006")

results_page_count={}
interval=1000

# define recording thread
recording_thread_stop_event = threading.Event()
def test_recording_thread(benchmark:str,data:list,interval:int, recording_thread_stop_event):
    while not recording_thread_stop_event.is_set():
        page_count=get_page_count()
        print(f"{benchmark}:{page_count}")
        data.append(page_count)
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
    init_scan()
    time.sleep(1)
    set_interval(interval)
    cgroup_utils.create_cgroup_dir(CGROUP_DIR)
    set_detect_flag()
    set_lazy_level(lazy)
    start_recording_thread(test_recording_thread,benchmark,tmp_data,interval)
    spec_utils.run_one_benchmark("test2-runspec.sh",benchmark)
    end_recording_thread()
    cgroup_utils.delete_cgroup_dir(CGROUP_DIR)
    clean_scan()
    results_page_count[benchmark]=tmp_data
    csv_utils.record(f"test2.csv",results_page_count)

for i in range(nproc):
    for benchmark in spec_utils.benchmarklist:
        run_one_time(benchmark)