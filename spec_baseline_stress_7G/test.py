from __future__ import absolute_import
import subprocess
import spec_utils
import time
from stress_utils import start_stress_memory, stop_stress
import os
import log_utils

nproc=1

kernelname=subprocess.getoutput("uname -r")
assert "spec-baseline-stress-7g" in kernelname

def set_nvm()->None:
    os.system("daxctl reconfigure-device --mode=system-ram dax0.0 -f")
    os.system("numastat -m")

def load_history()->list:
    result={}
    with open("experiment_history","r") as f:
        raw_lines=f.readlines()
        for line in raw_lines:
            raw_data=line.split(",")
            if len(raw_data)<2:
                continue
            benchmark=raw_data[0]
            benchmarkRuntime=float(raw_data[1])
            result[benchmark]=benchmarkRuntime
    return result

def save_history(result:dict)->list:
    with open("experiment_history","w") as f:
        for i in result:
            f.write(f"{i},{result[i]}\n")

spec_utils.set_path("/root/cpu2006")

results=load_history()

def run_one_time(benchmark:str):
    global results
    
    log_utils.log(f"Testing {benchmark}")
    spec_utils.setup_one_benchmark(benchmark)
    spec_utils.clean_log()
    start_stress_memory(1,7168,True)
    time.sleep(10)
    spec_utils.run_one_benchmark("runspec.sh",benchmark)
    stop_stress()
    benchmark_runtime=spec_utils.get_runtime_by_log(spec_utils.get_log())
    spec_utils.clean_one_benchmark(benchmark)
    results[benchmark]=benchmark_runtime
    data={
        'experiment':'spec-baseline-stress-7G',
        'benchmark':benchmark,
        'runtime':benchmark_runtime
    }
    log_utils.data_upload(data)
    save_history(results)
    os.system("reboot")
    time.sleep(10)

set_nvm()
for benchmark in spec_utils.benchmarklist:
    if benchmark in results:
        continue
    run_one_time(benchmark)

log_utils.log("测试完毕")