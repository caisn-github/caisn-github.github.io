from __future__ import absolute_import
import spec_utils
import time
from stress_utils import start_stress_memory, stop_stress
import udebugfs
import os
import cgroup_utils
import csv_utils

nproc=1

# kernelname=subprocess.getoutput("uname -r")
# assert "test1" in kernelname

with open("machinename") as f:
    MachineName=f.read().strip()

def log(message):
    print(message)

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

spec_utils.set_path("/root/cpu2006")

results_benchmark_runtime={}
interval=1000

def run_one_time(benchmark:str):
    if benchmark not in results_benchmark_runtime:
        results_benchmark_runtime[benchmark]=[]
    round_index=len(results_benchmark_runtime[benchmark])+1
    log(f"正在测试：{benchmark}:第{round_index}轮")
    spec_utils.setup_one_benchmark(benchmark)
    spec_utils.clean_log()
    set_interval(interval)
    init_scan()
    time.sleep(1)
    disable_migrate()
    set_migrate_max_count(1000)
    start_stress_memory(1,7168,True)
    time.sleep(10)
    cgroup_utils.mount_cgroup_root_dir(CGROUP_ROOT_DIR,"repabp")
    cgroup_utils.create_cgroup_dir(CGROUP_DIR)
    set_detect_flag()
    spec_utils.run_one_benchmark("optimize-runspec.sh",benchmark)
    cgroup_utils.delete_cgroup_dir(CGROUP_DIR)
    disable_migrate()
    clean_scan()
    stop_stress()
    benchmark_runtime=spec_utils.get_runtime_by_log(spec_utils.get_log())
    spec_utils.clean_one_benchmark(benchmark)
    results_benchmark_runtime[benchmark].append(benchmark_runtime)
    csv_utils.record(f"optimize-benchmark_runtime.csv",results_benchmark_runtime)

set_nvm()
for i in range(nproc):
    for benchmark in spec_utils.benchmarklist:
        run_one_time(benchmark)
        # break
