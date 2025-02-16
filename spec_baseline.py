from __future__ import absolute_import
import spec_utils
import zmq
import subprocess
import log_utils
import csv_utils

nproc=5

kernelname=subprocess.getoutput("uname -r")
assert "spec_baseline" in kernelname

with open("machinename") as f:
    MachineName=f.read().strip()

context=zmq.Context()

def log(message):
    print(message)
    log_utils.send(context, f"{MachineName}:{message}")

spec_utils.set_path("/root/cpu2006")

results_spec_runtime={}
# define running process

def run_one_time(benchmark:str):
    if benchmark not in results_spec_runtime:
        results_spec_runtime[benchmark]=[]
    log(f"正在测试：{benchmark}")
    spec_utils.setup_one_benchmark(benchmark)
    spec_utils.clean_log()
    spec_utils.run_one_benchmark("spec_baseline-runspec.sh",benchmark)
    benchmark_runtime=spec_utils.get_runtime_by_log(spec_utils.get_log())
    results_spec_runtime[benchmark].append(benchmark_runtime)
    spec_utils.clean_one_benchmark(benchmark)
    csv_utils.record(f"spec_baseline-spec_runtime.csv",results_spec_runtime)

for i in range(nproc):
    for benchmark in spec_utils.benchmarklist:
        run_one_time(benchmark)

# if not test_flag:
#     for benchmark in spec_utils.benchmarklist:
#         statistic, p_value = normaltest(results[benchmark])
#         alpha = 0.05
#         if p_value >= alpha:
#             break
#         else:
#             log(f"{benchmark}不符合正态分布")
