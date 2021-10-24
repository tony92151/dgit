import argparse
import json
import os
from .utils import command_run


# def dgit_init(dgit_path, submodule):
#     with open(dgit_path, "w") as f:
#         json.dump({"submodule": submodule}, f, indent=4, sort_keys=True)

def dgit_git(unknownargs):
    com = "git "
    for a in unknownargs:
        com += "{} ".format(a)

    command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "git command"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "git",
            help=self.command_help,
        )
        # self.parser.add_argument('--submodule',
        #                          type=str,
        #                          default=None,
        #                          help="path to submodule",
        #                          required=True
        #                          )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        dgit_git(unknownargs)
        # print(args.w)
