import argparse
import json
import os


def dgit_read(dgit_path):
    with open(dgit_path, "r") as f:
        contant = json.load(f)
    return contant


import sys
import subprocess


DGIT_DATA_FILE = ".dvc/DGITFILE"

def roll_output(proc, file=None):
    # https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-using-python
    while True:
        output = proc.stdout.readline()
        if proc.poll() is not None:
            break
        if output:
            if file is None:
                print(output.decode('utf-8').splitlines()[0])
            else:
                f = open(file, "a")
                f.write(output + "\n")
                f.close()

    rc = proc.poll()
    print("End output, PID : {}".format(proc.pid))


def command_run(command):
    print("\n $ {}".format(command))
    print("\n")
    proc = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE)
    roll_output(proc)
    proc.wait()
