import argparse
import os
import subprocess

from .utils import command_run, DGIT_DATA_FILE


# dvc add --no-commit

def check_s3_key():
    if os.getenv("AWS_ACCESS_KEY_ID", None) is None:
        os.environ["AWS_ACCESS_KEY_ID"] = input("AWS_ACCESS_KEY_ID=")

    if os.getenv("AWS_SECRET_ACCESS_KEY", None) is None:
        os.environ["AWS_SECRET_ACCESS_KEY"] = input("AWS_SECRET_ACCESS_KEY=")


def dgit_push(dvc_path, args, unknowargs: list):
    # print("")
    # git push
    com = "git push && git push --tags"
    command_run(command=com)

    com = "dvc --cd {} push {}".format(dvc_path, DGIT_DATA_FILE)
    for a in unknowargs:
        com += "{} ".format(a)
    command_run(command=com)

class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "Updates remote refs using local refs and upload newest dataset to remote storage."
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "push",
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
        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        dgit_push(dvc_path,
                  args,
                  unknownargs)
        # from git import Repo
        # repo = Repo(path=os.path.join(".", dgit_read(os.path.join(".", ".dgit"))["submodule"]))
        # if args.tags:
        #     for i, v in enumerate(repo.tags):
        #         print("({}) {}".format(i, v))
