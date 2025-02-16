import subprocess
import os

def read_from_debugfs_u64(path:str)->int:
    assert os.path.exists(path)
    return int(subprocess.getoutput(f"cat {path}"))

def write_to_debugfs_u64(path:str, value:int)->None:
    assert os.path.exists(path)
    subprocess.getoutput(f"echo {value} > {path}")

def write_to_debugfs_file(path:str, value:str)->None:
    assert os.path.exists(path)
    subprocess.getoutput(f"echo {value} > {path}")

def read_from_debugfs_file_by_bits(path:str,amount:int)->bytearray:
    result=bytearray(amount)
    with open(path,'rb') as file:
        ret=file.readinto(result)
    return result
