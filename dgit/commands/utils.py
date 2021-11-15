import argparse
import json
import os


def dgit_read(dgit_path):
    with open(dgit_path, "r") as f:
        contant = json.load(f)
    return contant


import sys
import subprocess

DGIT_DATA_FILE = ".dgit/DGITFILE.dvc"


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


def check_git_path(path="."):
    if os.getenv("DVC_REPO_PATH", None) is None:
        path = os.path.abspath(path)
        while not path == "/":
            path = os.path.dirname(path)
            if os.path.isdir(os.path.join(path, ".git")):
                break
        os.environ["DVC_REPO_PATH"] = path


def command_run(command, result=False):
    print("\n $ {}".format(command))
    print("\n")
    proc = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE)
    roll_output(proc)

    # stdout, stderr = proc.communicate()
    # exit_code = proc.wait()
    # print(stdout, stderr, exit_code)
    proc.wait()
    # return stdout, stderr, exit_code
