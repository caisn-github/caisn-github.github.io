import os, subprocess

benchmarklist = [
    # "400.perlbench",
    # "401.bzip2",
    # "403.gcc",
    # "410.bwaves",
    # "416.gamess",
    # "429.mcf",
    # "433.milc",
    # "434.zeusmp",
    # "435.gromacs",
    # "436.cactusADM",
    # "437.leslie3d",
    # "444.namd",
    # "445.gobmk",
    # "447.dealII",
    # "450.soplex",
    # "453.povray",
    # "454.calculix",
    # "456.hmmer",
    # "458.sjeng",
    # "459.GemsFDTD",
    # "462.libquantum",
    # "464.h264ref",
    # "465.tonto",
    # "470.lbm",
    # "471.omnetpp",
    # "473.astar",
    # "481.wrf",
    # "482.sphinx3",
    "483.xalancbmk",
]
dir_path=None
def set_path(path:str)->None:
    global dir_path
    dir_path=path

def clean_log()-> None:
    assert dir_path is not None
    os.system(f"rm -rf {dir_path}/result/*")

def setup_one_benchmark(benchmark:str)->None:
    assert dir_path is not None
    subprocess.getoutput(f"cd {dir_path} && \
                         source shrc && \
                         runspec --action=setup --config=my.cfg --size=ref --iterations=1 --tune=base --nobuild --noreportable {benchmark}")

def run_one_benchmark(path:str,benchmark:str)->None:
    assert dir_path is not None
    subprocess.getoutput(f"bash {path} {benchmark}")

def clean_one_benchmark(benchmark:str)->None:
    assert dir_path is not None
    subprocess.getoutput(f"cd {dir_path} && \
                         source shrc && \
                         runspec --action=clean --config=my.cfg --size=ref --iterations=1 --tune=base --nobuild --noreportable {benchmark}")

def get_log() -> str:
    assert dir_path is not None
    content=subprocess.getoutput(f"cd {dir_path} && cat {dir_path}/result/CPU2006.001.log")
    return content

def get_runtime_by_log(content:str)->float:
    for line in content.split("\n"):
        if "ratio" in line and "runtime" in line:
            index=line.find("runtime=")+len("runtime=")
            line=line[index:]
            index=line.find(",")
            line=line[:index]
            return float(line)