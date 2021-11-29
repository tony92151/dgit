import argparse
import os
import subprocess

from .utils import command_run, DGIT_DATA_FILE, locate_dgit_path


# dvc add --no-commit

def run_dvc_add(dgit_path, args, unknowargs: list):
    if not os.path.isfile(DGIT_DATA_FILE):
        add_ignore = True
    else:
        add_ignore = False

    com = "dvc --cd {} add --no-commit --file {} ".format(dgit_path, DGIT_DATA_FILE)
    for a in unknowargs:
        com += "{} ".format(a)
    command_run(command=com)

    com = "git add {}".format(DGIT_DATA_FILE)
    command_run(command=com)

    if add_ignore:
        com = "git add .gitignore"
        command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "Stage file for next commit."
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "add",
            help=self.command_help,
        )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        dgit_path = locate_dgit_path()

        # check if unknownargs > 0, because "dvc add" must have one  arg
        if len(unknownargs) < 1:
            self.parser.print_help()
            exit(1)
        run_dvc_add(dgit_path,
                    args,
                    unknownargs)
