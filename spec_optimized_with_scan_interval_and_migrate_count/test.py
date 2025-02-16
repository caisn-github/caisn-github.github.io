from __future__ import absolute_import
import subprocess
import spec_utils
import time
from stress_utils import start_stress_memory, stop_stress
import os
import log_utils
import cgroup_utils
import udebugfs

nproc=1

kernelname=subprocess.getoutput("uname -r")
assert "spec-optimized-with-scan-interval-and-migrate-count" in kernelname

def set_nvm()->None:
    os.system("daxctl reconfigure-device --mode=system-ram dax0.0 -f")
    os.system("numastat -m")

DEBUGFS_DIR="/sys/kernel/debug/repabp"
DEBUGFS_CONTROL_FILE=f"{DEBUGFS_DIR}/control"
DEBUGFS_INTERVAL_FILE=f"{DEBUGFS_DIR}/scan_interval"
DEBUGFS_READ_HISTORY_FILE=f"{DEBUGFS_DIR}/read_history"
DEBUGFS_MAX_PFN_FILE=f"{DEBUGFS_DIR}/max_pfn"
DEBUGFS_MIGRATE_ENABLE_FILE=f"{DEBUGFS_DIR}/migrate_enable"
DEBUGFS_MIGRATE_MAX_COUNT_FILE=f"{DEBUGFS_DIR}/migrate_max_count"

CGROUP_ROOT_DIR="/repabp"
CGROUP_DIR=f"{CGROUP_ROOT_DIR}/test"
CGROUP_DETECT_FLAG_FILE=f"{CGROUP_DIR}/repabp.detect_flag"
CGROUP_TASK_FILE=f"{CGROUP_DIR}/tasks"

def init_scan()->None:
    udebugfs.write_to_debugfs_file(DEBUGFS_CONTROL_FILE,"init")

def clean_scan()->None:
    udebugfs.write_to_debugfs_file(DEBUGFS_CONTROL_FILE,"clean")

def set_interval(interval:int)->None:
    udebugfs.write_to_debugfs_u64(DEBUGFS_INTERVAL_FILE,interval)

def enable_migrate()->None:
    udebugfs.write_to_debugfs_u64(DEBUGFS_MIGRATE_ENABLE_FILE,1)

def disable_migrate()->None:
    udebugfs.write_to_debugfs_u64(DEBUGFS_MIGRATE_ENABLE_FILE,0)

def set_migrate_max_count(count:int)->None:
    udebugfs.write_to_debugfs_u64(DEBUGFS_MIGRATE_MAX_COUNT_FILE,count)

def set_detect_flag()->None:
    assert os.path.exists(CGROUP_DETECT_FLAG_FILE)
    os.system(f"echo 1 > {CGROUP_DETECT_FLAG_FILE}")

class record:
    def __init__(self,scan_interval:int,migrate_count:int,runtime:float) -> None:
        self.scan_interval=scan_interval
        self.migrate_count=migrate_count
        self.runtime=runtime

def load_history()->list:
    result=[]
    with open("experiment_history","r") as f:
        raw_lines=f.readlines()
        for line in raw_lines:
            raw_data=line.split(",")
            if len(raw_data)<2:
                continue
            scan_interval=int(raw_data[0])
            migrate_count=int(raw_data[1])
            benchmarkRuntime=float(raw_data[2])
            result.append(record(scan_interval,migrate_count,benchmarkRuntime))
    return result

def save_history(result:list)->list:
    with open("experiment_history","w") as f:
        for i in result:
            f.write(f"{i.scan_interval},{i.migrate_count},{i.runtime}\n")

spec_utils.set_path("/root/cpu2006")

results=load_history()

def run_one_time(scan_interval:int, migrate_count:int):
    global results
    
    log_utils.log(f"Testing 400.perlbench")
    spec_utils.setup_one_benchmark("400.perlbench")
    spec_utils.clean_log()
    set_interval(scan_interval)
    init_scan()
    time.sleep(1)
    enable_migrate()
    set_migrate_max_count(migrate_count)
    start_stress_memory(1,7168,True)
    time.sleep(10)
    cgroup_utils.mount_cgroup_root_dir(CGROUP_ROOT_DIR,"repabp")
    cgroup_utils.create_cgroup_dir(CGROUP_DIR)
    set_detect_flag()
    spec_utils.run_one_benchmark("runspec.sh","400.perlbench")
    cgroup_utils.delete_cgroup_dir(CGROUP_DIR)
    disable_migrate()
    clean_scan()
    stop_stress()
    benchmark_runtime=spec_utils.get_runtime_by_log(spec_utils.get_log())
    spec_utils.clean_one_benchmark("400.perlbench")
    results.append(record(scan_interval=scan_interval,migrate_count=migrate_count,runtime=benchmark_runtime))
    data={
        'scan_interval':scan_interval,
        'migrate_count':migrate_count,
        'runtime':benchmark_runtime
    }
    log_utils.data_upload("spec_optimized_with_scan_interval_and_migrate_count", data)
    save_history(results)
    os.system("reboot")
    time.sleep(10)

set_nvm()
scan_intervals=[i for i in range(200,2200,200)]
migrate_counts=[i for i in range(200,2200,200)]
for scan_interval in scan_intervals:
    for migrate_count in migrate_counts:
        skip_flag=False
        for i in results:
            if i.scan_interval==scan_interval and i.migrate_count==migrate_count:
                skip_flag=True
                break
        if skip_flag:
            continue
        run_one_time(scan_interval,migrate_count)

log_utils.log("测试完毕")