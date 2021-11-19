import argparse
import os
from git import Repo
from .utils import command_run, DGIT_DATA_FILE, locate_dgit_path, print_tags, check_s3_key


def dgit_data_pull(dvc_path, args, unknownargs):
    check_s3_key()
    com = "dvc --cd {} pull {}".format(dvc_path, DGIT_DATA_FILE)
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
        print(unknownargs)
        dgit_path = locate_dgit_path()

        repo = Repo(path=dgit_path)

        selected_tag = print_tags(repo=repo, with_selection=True)

        repo.git.checkout(selected_tag, os.path.join(DGIT_DATA_FILE))
        print("\ngit checkout to : ", selected_tag)

        dgit_data_pull(dgit_path, args, unknownargs)
