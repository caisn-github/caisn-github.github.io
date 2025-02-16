from __future__ import absolute_import
import subprocess
import spec_utils
import time
from stress_utils import start_stress_memory, stop_stress
import os
##import log_utils

nproc=1

kernelname=subprocess.getoutput("uname -r")
##assert "spec-motivation-stress" in kernelname

def set_nvm()->None:
    os.system("daxctl reconfigure-device --mode=system-ram dax0.0 -f")
    os.system("numastat -m")

class record:
    def __init__(self,benchmark:str,stress:int,runtime:float) -> None:
        self.benchmark=benchmark
        self.stress=stress
        self.runtime=runtime

def load_history()->list:
    result=[]
    with open("experiment_history","r") as f:
        raw_lines=f.readlines()
        for line in raw_lines:
            raw_data=line.split(",")
            if len(raw_data)<2:
                continue
            benchmark=raw_data[0]
            stress=int(raw_data[1])
            benchmarkRuntime=float(raw_data[2])
            result.append(record(benchmark,stress,benchmarkRuntime))
    return result

def save_history(result:list)->list:
    with open("experiment_history","w") as f:
        for i in result:
            f.write(f"{i.benchmark},{i.stress},{i.runtime}\n")

spec_utils.set_path("/root/cpu2006")

results=load_history()

def run_one_time(benchmark:str,stress:int):
    global results
    
    print(f"Testing {benchmark} {stress}")
    spec_utils.setup_one_benchmark(benchmark)
    spec_utils.clean_log()
    start_stress_memory(1,stress,True)
    time.sleep(10)
    spec_utils.run_one_benchmark("runspec.sh",benchmark)
    stop_stress()
    benchmark_runtime=spec_utils.get_runtime_by_log(spec_utils.get_log())
    spec_utils.clean_one_benchmark(benchmark)
    results.append(record(benchmark=benchmark,stress=stress,runtime=benchmark_runtime))
    data={
        'benchmark':benchmark,
        'stress':stress,
        'runtime':benchmark_runtime
    }
    ##log_utils.data_upload('spec_motivation_stress',data)
    save_history(results)
    os.system("reboot")
    time.sleep(10)

stress_list=[
    1024,
    2048,
    3072,
    4096,
    5120,
    5632,
    6144,
    6656,
    7168,
    7680,
    8192
]

set_nvm()
for benchmark in spec_utils.benchmarklist:
    for stress in stress_list:
        skip_flag=False
        for i in results:
            if i.benchmark==benchmark and i.stress==stress:
                skip_flag=True
                break
        if skip_flag:
            continue
        run_one_time(benchmark,stress)

print("测试完毕")
