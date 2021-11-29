import argparse
import os
import git
from git import Repo
from .utils import command_run, DGIT_DATA_FILE, locate_dgit_path, print_tags, check_s3_key
import logging


def dgit_checkout(dgit_path, repo: Repo, selected_tag, args, unknowargs: list):

    try:
        repo.git.checkout(selected_tag)
    except git.exc.GitCommandError:
        logging.error("tag not match.")
        exit(1)

    if args.without_data:
        pass
    else:
        check_s3_key()
        com = "dvc --cd {} pull {}".format(dgit_path, DGIT_DATA_FILE)
        command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "Checkout to specific version."
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "checkout",
            help=self.command_help,
        )

        # self.parser.add_argument(
        #     '--list-tags',
        #     help='list all tags and select.',
        #     action='store_true'
        # )

        self.parser.add_argument(
            '--without-data',
            help='(develop) pull {} only'.format(DGIT_DATA_FILE),
            action='store_true'
        )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        dgit_path = locate_dgit_path()
        repo = Repo(path=dgit_path)

        if len(unknownargs) > 1:
            logging.warning("Expect one argument but got multiple arguments. Please retry.")
            exit(1)
        selected_tag = unknownargs[0]

        dgit_checkout(dgit_path,
                      repo,
                      selected_tag,
                      args,
                      unknownargs)
