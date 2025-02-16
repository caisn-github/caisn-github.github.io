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
assert "motivation-page-allocation-count" in kernelname

def set_nvm()->None:
    os.system("daxctl reconfigure-device --mode=system-ram dax0.0 -f")
    os.system("numastat -m")

DEBUGFS_DIR="/sys/kernel/debug/repabp"
DEBUGFS_PAGE_ALLOCATION_COUNT=f"{DEBUGFS_DIR}/page_allocation_count"
DEBUGFS_CONTROL_ENABLE=f"{DEBUGFS_DIR}/control_enable"

CGROUP_ROOT_DIR="/repabp"
CGROUP_DIR=f"{CGROUP_ROOT_DIR}/test"
CGROUP_DETECT_FLAG_FILE=f"{CGROUP_DIR}/repabp.detect_flag"
CGROUP_TASK_FILE=f"{CGROUP_DIR}/tasks"

def get_page_allocation_count()->int:
    return udebugfs.read_from_debugfs_u64(DEBUGFS_PAGE_ALLOCATION_COUNT)

def set_page_allocation_count(data:int)->None:
    udebugfs.write_to_debugfs_u64(DEBUGFS_PAGE_ALLOCATION_COUNT,data)

def set_control_enable(data:int)->None:
    udebugfs.write_to_debugfs_u64(DEBUGFS_CONTROL_ENABLE,data)

def set_detect_flag()->None:
    assert os.path.exists(CGROUP_DETECT_FLAG_FILE)
    os.system(f"echo 1 > {CGROUP_DETECT_FLAG_FILE}")

spec_utils.set_path("/root/cpu2006")

interval=1000

# define recording thread
recording_thread_stop_event = threading.Event()
def test_recording_thread(benchmark:str,data:dict,interval:int, recording_thread_stop_event):
    index=0
    while not recording_thread_stop_event.is_set():
        data['index'].append(index)
        data['page_allocation_count'].append(get_page_allocation_count())
        index+=1
        set_page_allocation_count(0)
        time.sleep(interval/1000)

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
    tmp_data={'index':[], "page_allocation_count":[]}
    spec_utils.setup_one_benchmark(benchmark)
    spec_utils.clean_log()
    time.sleep(1)
    cgroup_utils.mount_cgroup_root_dir(CGROUP_ROOT_DIR,"repabp")
    cgroup_utils.create_cgroup_dir(CGROUP_DIR)
    set_page_allocation_count(0)
    set_detect_flag()
    start_recording_thread(benchmark,tmp_data,interval)
    set_control_enable(1)
    spec_utils.run_one_benchmark("runspec.sh",benchmark)
    set_control_enable(0)
    end_recording_thread()
    cgroup_utils.delete_cgroup_dir(CGROUP_DIR)
    spec_utils.clean_one_benchmark(benchmark)
    for i,_ in enumerate(tmp_data['index']):
        data={
            'benchmark':benchmark,
            'index':tmp_data['index'][i],
            'page_allocation_count':tmp_data['page_allocation_count'][i]
        }
        log_utils.data_upload("motivation_page_allocation_count",data)

with open("../machine.txt","r") as f:
    machineName=f.read().strip()

set_nvm()
if machineName=='NVM-1':
    benchmark='400.perlbench'
elif machineName=='NVM-2':
    benchmark='401.bzip2'
elif machineName=='NVM-3':
    benchmark='403.gcc'
    
run_one_time(benchmark)

log_utils.log("测试完毕")