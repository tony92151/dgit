import argparse
import os
from git import Repo
from .utils import command_run, DGIT_DATA_FILE


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "checkout to different version."
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "checkout",
            help=self.command_help,
        )

        self.parser.add_argument(
            '--list-tags',
            help='list all tags and select.',
            action='store_true'
        )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        print(unknownargs)
        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        if len(unknownargs) < 1:
            self.parser.print_help()

        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        repo = Repo(path=dvc_path)

        if args.list_tags:
            for i, v in enumerate(repo.tags):
                print("({}) {}".format(i, v))

            selected_tag = str(repo.tags[int(input("? "))])
        else:
            selected_tag = unknownargs[0]
        repo.git.checkout(selected_tag)

