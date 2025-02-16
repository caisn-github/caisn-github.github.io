from __future__ import absolute_import
import spec_utils
import time
import zmq
import subprocess
import log_utils
import udebugfs
import os
import threading
import cgroup_utils
import csv_utils

nproc=2
lazy=4

kernelname=subprocess.getoutput("uname -r")
##assert "test1" in kernelname
assert "csn" in kernelname

#with open("machinename") as f:
#    MachineName=f.read().strip()

context=zmq.Context()

def log(message):
    print(message)
    ##log_utils.send(context, f"{MachineName}:{message}")

DEBUGFS_DIR="/sys/kernel/debug/repabp"
DEBUGFS_CONTROL_FILE=f"{DEBUGFS_DIR}/control"
DEBUGFS_INTERVAL_FILE=f"{DEBUGFS_DIR}/scan_interval"
DEBUGFS_LAZY_LEVEL_FILE=f"{DEBUGFS_DIR}/lazy_level"
DEBUGFS_SCAN_INDEX_FILE=f"{DEBUGFS_DIR}/scan_index"
DEBUGFS_SCAN_TIME_FILE=f"{DEBUGFS_DIR}/scan_time"
DEBUGFS_SCAN_AMOUNT_FILE=f"{DEBUGFS_DIR}/scan_amount"
DEBUGFS_READ_FILE=f"{DEBUGFS_DIR}/read"
DEBUGFS_READ_ARRAY_FILE="/dev/memory_detector_history"
CGROUP_DIR="/sys/fs/cgroup/repabp/test"
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

def get_scan_index()->int:
    return udebugfs.read_from_debugfs_u64(DEBUGFS_SCAN_INDEX_FILE)

def get_scan_ntime()->int:
    return udebugfs.read_from_debugfs_u64(DEBUGFS_SCAN_TIME_FILE)

def get_scan_amount()->int:
    return udebugfs.read_from_debugfs_u64(DEBUGFS_SCAN_AMOUNT_FILE)

def set_detect_flag()->None:
    assert os.path.exists(CGROUP_DETECT_FLAG_FILE)
    os.system(f"echo 1 > {CGROUP_DETECT_FLAG_FILE}")

def record_thread():
    subprocess.getoutput("./record")

def start_recording()->None:
    os.system("echo 1 > ./runflag")
    t=threading.Thread(target=record_thread)
    t.start()

def end_recording()->None:
    os.system("echo 0 > ./runflag")
    while "0" not in subprocess.getoutput("cat ./record_lock"):
        time.sleep(0.1)

spec_utils.set_path("/root/cpu2006")

results_scan_time={}
results_scan_record_avg_time={}
results_benchmark_runtime={}
interval=1000

# define recording thread
recording_thread_stop_event = threading.Event()
def test_recording_thread(benchmark:str,data:dict,interval:int, recording_thread_stop_event):
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

def start_recording_thread(benchmark:str,data,interval:int)->None:
    global recording_thread_stop_event
    
    recording_thread_stop_event.clear()
    t=threading.Thread(target=test_recording_thread,args=(benchmark,data,interval,recording_thread_stop_event))
    t.start()

def end_recording_thread()->None:
    global recording_thread_stop_event
    
    recording_thread_stop_event.set()
    time.sleep(3)

def run_one_time(benchmark:str):
    if benchmark not in results_scan_time:
        results_scan_time[benchmark]=[]
    if benchmark not in results_scan_record_avg_time:
        results_scan_record_avg_time[benchmark]=[]
    if benchmark not in results_benchmark_runtime:
        results_benchmark_runtime[benchmark]=[]
    round_index=len(results_scan_time[benchmark])+1
    log(f"正在测试：{benchmark}:第{round_index}轮")
    tmp_data={'scan_time':[], "scan_record_avg_time":[]}
    spec_utils.setup_one_benchmark(benchmark)
    spec_utils.clean_log()
    init_scan()
    time.sleep(1)
    set_interval(interval)
    cgroup_utils.create_cgroup_dir(CGROUP_DIR)
    set_detect_flag()
    set_lazy_level(lazy)
    start_recording()
    start_recording_thread(benchmark,tmp_data,interval)
    spec_utils.run_one_benchmark("test1-runspec.sh",benchmark)
    end_recording_thread()
    end_recording()
    cgroup_utils.delete_cgroup_dir(CGROUP_DIR)
    clean_scan()
    benchmark_runtime=spec_utils.get_runtime_by_log(spec_utils.get_log())
    spec_utils.clean_one_benchmark(benchmark)
    scan_time_avg=sum(tmp_data['scan_time'])/len(tmp_data['scan_time'])
    scan_record_avg_time_avg=sum(tmp_data['scan_record_avg_time'])/len(tmp_data['scan_record_avg_time'])
    results_scan_time[benchmark].append(scan_time_avg)
    results_scan_record_avg_time[benchmark].append(scan_record_avg_time_avg)
    results_benchmark_runtime[benchmark].append(benchmark_runtime)
    csv_utils.record(f"lazy-{lazy}-scan_time.csv",results_scan_time)
    csv_utils.record(f"lazy-{lazy}-scan_record_avg_time.csv",results_scan_record_avg_time)
    csv_utils.record(f"lazy-{lazy}-benchmark_runtime.csv",results_benchmark_runtime)

for i in range(nproc):
    for benchmark in spec_utils.benchmarklist:
        run_one_time(benchmark)
