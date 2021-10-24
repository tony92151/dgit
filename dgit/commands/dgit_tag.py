import argparse
import os

from .utils import dgit_read


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "list the dvc"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "tag",
            help=self.command_help,
        )

        self.parser.add_argument(
            '--list',
            help='list all tags',
            action='store_true'
        )

        self.parser.add_argument(
            '--checkout',
            help='checkout selected tags',
            action='store_true'
        )
        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        from git import Repo
        repo = Repo(path=os.path.join(".", dgit_read(os.path.join(".", ".dgit"))["submodule"]))
        if args.list:
            for i, v in enumerate(repo.tags):
                print("({}) {}".format(i, v))

        if args.checkout:
            for i, v in enumerate(repo.tags):
                print("({}) {}".format(i, v))
            # inkey = input("? ")
            # if isinstance(inkey)
            selected_tag = str(repo.tags[int(input("? "))])
            repo.git.checkout(selected_tag, os.path.join("AI9_data_version.dvc"))
            print("\ngit checkout to : ", selected_tag)

