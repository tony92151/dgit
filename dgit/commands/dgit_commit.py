import argparse
import os
import subprocess

from .utils import command_run, locate_dgit_path


def run_dvc_commit(dgit_path, args, unknowargs: list):
    # dvc commit
    com = "dvc --cd {} commit ".format(dgit_path)
    for a in unknowargs:
        com += "{} ".format(a)
    command_run(command=com)

    # git commit
    com = "git commit -m '{}'".format(args.m)
    command_run(command=com)

    # git tag
    if args.force:
        # remove tag on remote(github)
        # git push origin :{tag}
        com = "git push origin :{} && git tag -d {} && git tag {} -a -m 'add tag {}'".format(
            args.tag, args.tag, args.tag, args.tag)
    else:
        com = "git tag {} -a -m 'add tag {}'".format(args.tag, args.tag)

    command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "Create a new commit containing staged files."
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "commit",
            help=self.command_help,
        )

        self.parser.add_argument(
            '--m',
            type=str,
            help='commit message.',
            required=True,
        )

        self.parser.add_argument(
            '--tag',
            type=str,
            help='name of tag to this commit.',
            required=True,
        )

        self.parser.add_argument(
            '--force',
            action="store_true",
            help='Replace existed tag.',
        )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        dgit_path = locate_dgit_path()

        run_dvc_commit(dgit_path,
                       args,
                       unknownargs)
