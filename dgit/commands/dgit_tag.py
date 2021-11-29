import argparse
import os
import git
from git import Repo
from .utils import command_run, DGIT_DATA_FILE, locate_dgit_path, print_tags
import logging


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "List all tags."
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "tag",
            help=self.command_help,
        )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        dgit_path = locate_dgit_path()
        repo = Repo(path=dgit_path)
        print_tags(repo=repo, with_info=True)
