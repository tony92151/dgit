import argparse
import os
import subprocess

from .utils import dgit_read, roll_output

# dvc add --no-commit

def check_s3_key():
    if os.getenv("AWS_ACCESS_KEY_ID", None) is None:
        os.environ["AWS_ACCESS_KEY_ID"] = input("AWS_ACCESS_KEY_ID=")

    if os.getenv("AWS_SECRET_ACCESS_KEY", None) is None:
        os.environ["AWS_SECRET_ACCESS_KEY"] = input("AWS_SECRET_ACCESS_KEY=")

def run_dvc_pull(dvc_path, unknowargs:list):
    # print("")
    com = "dvc --cd {} pull".format(dvc_path)
    for a in unknowargs:
        com+= "{} ".format(a)
    print("\n $ {}".format(com))
    print("\n")
    proc = subprocess.Popen(
        com, shell=True,
        stdout=subprocess.PIPE)
    roll_output(proc)
    proc.wait()

class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "dvc pull [args]"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "pull",
            help=self.command_help,
        )

        # self.parser.add_argument(
        #     '--tags',
        #     help='list all tags',
        #     action='store_true'
        # )
        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        print(unknownargs)
        print("\nCheck s3 key...")
        check_s3_key()
        run_dvc_pull(os.path.join(".", dgit_read(os.path.join(".", ".dgit"))["submodule"]),
                    unknownargs)
        # from git import Repo
        # repo = Repo(path=os.path.join(".", dgit_read(os.path.join(".", ".dgit"))["submodule"]))
        # if args.tags:
        #     for i, v in enumerate(repo.tags):
        #         print("({}) {}".format(i, v))
