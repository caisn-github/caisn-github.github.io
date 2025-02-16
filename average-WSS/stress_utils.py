import os
import subprocess
import threading

def _stress_thread(cmd:str):
    os.system(cmd)

def start_stress_memory(memory_nproc:int, space_MB:int, space_keep:bool):
    t=threading.Thread(target=_stress_thread,args=(f"stress --vm {memory_nproc} --vm-bytes {space_MB}M {'--vm-keep' if space_keep else ''}",))
    t.start()

def stop_stress():
    stress_pid_str=subprocess.getoutput("pgrep stress")
    stress_pids=stress_pid_str.split("\n")
    for stress_pid in stress_pids:
        os.system(f"kill {stress_pid}")