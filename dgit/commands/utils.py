import argparse
import json
import os
from git import Repo


def dgit_read(dgit_path):
    with open(dgit_path, "r") as f:
        contant = json.load(f)
    return contant


import sys
import subprocess


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


def locate_dgit_path(path="."):
    path = os.path.abspath(path)
    while not path == "/":
        if os.path.isdir(os.path.join(path, ".git")) and os.path.isdir(os.path.join(path, ".dvc")):
            break
        path = os.path.dirname(path)
    return path


def locate_git_path(path="."):
    path = os.path.abspath(path)
    while not path == "/":
        if os.path.isdir(os.path.join(path, ".git")):
            break
        path = os.path.dirname(path)
    return path


def print_tags(repo: Repo, with_selection=False):
    for i, v in enumerate(repo.tags):
        print("({}) {}".format(i, v))
    selected_tag = None
    if with_selection:
        selected_tag = str(repo.tags[int(input("? "))])
    return selected_tag


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


def check_s3_key():
    if os.getenv("AWS_ACCESS_KEY_ID", None) is None:
        os.environ["AWS_ACCESS_KEY_ID"] = input("AWS_ACCESS_KEY_ID=")

    if os.getenv("AWS_SECRET_ACCESS_KEY", None) is None:
        os.environ["AWS_SECRET_ACCESS_KEY"] = input("AWS_SECRET_ACCESS_KEY=")


DGIT_DATA_FILE = os.path.join(locate_dgit_path(), ".dgit/DGITFILE.dvc")
