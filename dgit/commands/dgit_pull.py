import argparse
import os
import subprocess
from git import Repo
from .utils import command_run, DGIT_DATA_FILE, locate_dgit_path, check_s3_key


# dvc add --no-commit

def dgit_pull(dvc_path, repo: Repo, args, unknowargs: list):
    # print("")
    o = repo.remotes.origin
    o.pull()

    com = "dvc --cd {} pull {}".format(dvc_path, DGIT_DATA_FILE)
    command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "Incorporates changes from a remote repository into the current branch and pull newest data from remote storage."
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "pull",
            help=self.command_help,
        )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        print(unknownargs)

        dgit_path = locate_dgit_path()

        repo = Repo(path=dgit_path)

        check_s3_key()

        dgit_pull(dgit_path,
                  repo,
                  args,
                  unknownargs)

