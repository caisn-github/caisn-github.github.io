from __future__ import absolute_import
import subprocess
import threading
import spec_utils
import time
from stress_utils import start_stress_memory, stop_stress
import os
import log_utils
import cgroup_utils
import udebugfs

nproc=1

kernelname=subprocess.getoutput("uname -r")
assert "wss-time" in kernelname

def set_nvm()->None:
    os.system("daxctl reconfigure-device --mode=system-ram dax0.0 -f")
    os.system("numastat -m")

DEBUGFS_DIR="/sys/kernel/debug/repabp"
DEBUGFS_PID=f"{DEBUGFS_DIR}/pid"
DEBUGFS_TRIGGER_SCAN_FILE=f"{DEBUGFS_DIR}/trigger_scan"
DEBUGFS_RSS_COUNT_FILE=f"{DEBUGFS_DIR}/rss_count"

# define debugfs operations
def trigger_scan():
    udebugfs.write_to_debugfs_u64(DEBUGFS_TRIGGER_SCAN_FILE,1)

def get_rss_count():
    return udebugfs.read_from_debugfs_u64(DEBUGFS_RSS_COUNT_FILE)

def set_rss_count(data:int)->None:
    udebugfs.write_to_debugfs_u64(DEBUGFS_RSS_COUNT_FILE,data)

# class record:
#     def __init__(self,benchmark:str,average_WSS:float) -> None:
#         self.benchmark=benchmark
#         self.average_WSS=average_WSS

# def load_history()->list:
#     result=[]
#     with open("experiment_history","r") as f:
#         raw_lines=f.readlines()
#         for line in raw_lines:
#             raw_data=line.split(",")
#             if len(raw_data)<2:
#                 continue
#             benchmark=raw_data[0]
#             average_WSS=float(raw_data[1])
#             result.append(record(benchmark,average_WSS))
#     return result

# def save_history(result:list)->list:
#     with open("experiment_history","w") as f:
#         for i in result:
#             f.write(f"{i.benchmark},{i.average_WSS}\n")

spec_utils.set_path("/root/cpu2006")

# results=load_history()
results=[]
interval=1000

# define recording thread
recording_thread_stop_event = threading.Event()
def test_recording_thread(benchmark:str,data:dict,interval:int, recording_thread_stop_event):
    index=0
    while not recording_thread_stop_event.is_set():
        trigger_scan()
        rss_count=get_rss_count()
        data['index'].append(index)
        data['WSS'].append(rss_count)
        set_rss_count(0)
        time.sleep(1)
        index+=1

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
    global results
    
    log_utils.log(f"Testing {benchmark}")
    tmp_data={"index":[],"WSS":[]}
    spec_utils.setup_one_benchmark(benchmark)
    spec_utils.clean_log()
    time.sleep(1)
    start_recording_thread(benchmark,tmp_data,interval)
    spec_utils.run_one_benchmark("runspec.sh",benchmark)
    end_recording_thread()
    spec_utils.clean_one_benchmark(benchmark)
    # results.append(record(benchmark=benchmark,average_WSS=average_WSS))
    for i,_ in enumerate(tmp_data["index"]):
        data={
            'benchmark':benchmark,
            'index':tmp_data["index"][i],
            'WSS':tmp_data['WSS'][i]
        }
        log_utils.data_upload("WSS_time",data)
    # save_history(results)
    os.system("reboot")
    time.sleep(10)


set_nvm()
with open("../machine.txt","r") as f:
    machineName=f.read().strip()
if machineName=="NVM-1":
    benchmark="453.povray"
elif machineName=="NVM-2":
    benchmark="429.mcf"
else:
    exit(0)
run_one_time(benchmark)
log_utils.log("测试完毕")