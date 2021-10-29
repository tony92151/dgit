import argparse
import os
from git import Repo
from .utils import command_run, DGIT_DATA_FILE

from .dgit_pull import check_s3_key


def dgit_data_pull(dvc_path, args, unknownargs):
    check_s3_key()
    com = "dvc --cd {} pull".format(dvc_path)
    command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "dvc data pull"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "data_pull",
            help=self.command_help,
        )
        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        repo = Repo(path=dvc_path)

        for i, v in enumerate(repo.tags):
            print("({}) {}".format(i, v))

        selected_tag = str(repo.tags[int(input("? "))])
        repo.git.checkout(selected_tag, os.path.join(DGIT_DATA_FILE))
        print("\ngit checkout to : ", selected_tag)

        dgit_data_pull(dvc_path, args, unknownargs)
