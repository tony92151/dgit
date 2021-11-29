import argparse
import json
import os
from git import Repo
import pandas as pd


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
        if os.path.isdir(os.path.join(path, ".git")) and os.path.isdir(os.path.join(path, ".dgit")):
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


def print_tags(repo: Repo, with_info=False):
    if with_info:
        tags = repo.tags
        tags_info = []
        for t in repo.tags:
            tags_info.append([str(t), t.commit.committed_datetime])
        df = pd.DataFrame(tags_info, columns=['Tag', 'Time'])
        df = df.sort_values(by='Time')
        print(df)
    else:
        for i, v in enumerate(repo.tags):
            print("({}) {}".format(i, v))


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


def check_s3_key_isvalid():
    if (os.getenv("AWS_ACCESS_KEY_ID", None) is not None) and (os.getenv("AWS_SECRET_ACCESS_KEY", None) is not None):
        return (len(os.getenv("AWS_ACCESS_KEY_ID", None)) == 20) and (
                len(os.getenv("AWS_SECRET_ACCESS_KEY", None)) == 40)
    else:
        return False


def check_s3_key():
    print("\nCheck s3 key...")

    if os.path.isfile(os.join(locate_dgit_path(), ".dgit", "key.key")):
        with open(os.join(locate_dgit_path(), ".dgit", "key.key"), "r") as f:
            key = json.load(f)
        os.environ["AWS_ACCESS_KEY_ID"] = key["AWS_ACCESS_KEY_ID"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = key["AWS_SECRET_ACCESS_KEY"]
    else:
        if os.getenv("AWS_ACCESS_KEY_ID", None) is None:
            os.environ["AWS_ACCESS_KEY_ID"] = input("AWS_ACCESS_KEY_ID=")

        if os.getenv("AWS_SECRET_ACCESS_KEY", None) is None:
            os.environ["AWS_SECRET_ACCESS_KEY"] = input("AWS_SECRET_ACCESS_KEY=")

    if not check_s3_key_isvalid():
        print("s3 key is not valid. Please try again")
        exit(1)


DGIT_DATA_FILE = os.path.join(locate_dgit_path(), ".dgit/DGITFILE.dvc")
