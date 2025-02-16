import os
import threading
import subprocess
import time
import udebugfs

SCAN_DIR="/sys/kernel/debug/memory_detector"
SCAN_CONTROL_FILE=f"{SCAN_DIR}/control"
SCAN_INTERVAL_FILE=f"{SCAN_DIR}/scan_interval"
SCAN_LAZY_LEVEL_FILE=f"{SCAN_DIR}/lazy_level"
SCAN_CGROUP_DIR="/sys/fs/cgroup/memory_detector/test"
SCAN_CGROUP_DETECT_FLAG_FILE=f"{SCAN_CGROUP_DIR}/memory_detector.detect_flag"
SCAN_CGROUP_TASK_FILE=f"{SCAN_CGROUP_DIR}/tasks"
SCAN_INDEX_FILE=f"{SCAN_DIR}/scan_index"
SCAN_TIME_FILE=f"{SCAN_DIR}/scan_time"
SCAN_AMOUNT_FILE=f"{SCAN_DIR}/scan_amount"
SCAN_READ_FILE=f"{SCAN_DIR}/read"
SCAN_READ_ARRAY_FILE="/dev/memory_detector_history"

assert os.path.exists(SCAN_DIR)

def init_scan()->None:
    udebugfs.write_to_debugfs_file(SCAN_CONTROL_FILE,"init")

def set_interval(interval:int)->None:
    udebugfs.write_to_debugfs_u64(SCAN_INTERVAL_FILE,interval)

def create_cgroup_dir()->None:
    if not os.path.exists(SCAN_CGROUP_DIR):
        os.system(f"mkdir {SCAN_CGROUP_DIR}")
    assert os.path.exists(SCAN_CGROUP_TASK_FILE)

def set_detect_flag()->None:
    assert os.path.exists(SCAN_CGROUP_DETECT_FLAG_FILE)
    os.system(f"echo 1 > {SCAN_CGROUP_DETECT_FLAG_FILE}")

def clean_scan()->None:
    udebugfs.write_to_debugfs_file(SCAN_CONTROL_FILE,"clean")

def delete_cgroup_dir()->None:
    assert os.path.exists(SCAN_CGROUP_TASK_FILE)
    os.system(f"rmdir {SCAN_CGROUP_DIR}")
    assert not os.path.exists(SCAN_CGROUP_TASK_FILE)

def get_scan_index()->int:
    return udebugfs.read_from_debugfs_u64(SCAN_INDEX_FILE)

def get_scan_ntime()->int:
    return udebugfs.read_from_debugfs_u64(SCAN_TIME_FILE)

def get_scan_amount()->int:
    return udebugfs.read_from_debugfs_u64(SCAN_AMOUNT_FILE)

def set_lazy_level(level:int)->None:
    udebugfs.write_to_debugfs_u64(SCAN_LAZY_LEVEL_FILE, level)

recording_thread_stop_event = threading.Event()
def test_recording_thread(benchmark:str,data:dict,interval:int,recording_thread_stop_event):
    index_cached=0
    while not recording_thread_stop_event.is_set():
        index=get_scan_index()
        ntime=get_scan_ntime()
        amount=get_scan_amount()
        if amount!=0:
            scan_record_avg_time=ntime/amount
        if index!=index_cached and index!=0:
            data["scan_time"].append(ntime)
            data["scan_record_avg_time"].append(scan_record_avg_time)
        index=index_cached
        time.sleep(interval/1000*0.9)

def start_test_recording(benchmark:str,data:dict,interval:int)->None:
    global recording_thread_stop_event
    
    recording_thread_stop_event.clear()
    t=threading.Thread(target=test_recording_thread,args=(benchmark,data,interval,recording_thread_stop_event))
    t.start()

def end_test_recording()->None:
    global recording_thread_stop_event
    recording_thread_stop_event.set()
    time.sleep(3)

def record_thread():
    subprocess.getoutput("./record")
    # os.system("./record")

def start_recording()->None:
    os.system("echo 1 > ./runflag")
    t=threading.Thread(target=record_thread)
    t.start()

def end_recording()->None:
    os.system("echo 0 > ./runflag")
    while "0" not in subprocess.getoutput("cat ./record_lock"):
        time.sleep(0.1)
