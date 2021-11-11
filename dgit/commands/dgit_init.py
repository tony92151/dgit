import argparse
import json
import os
from .utils import command_run


# def dgit_init(dgit_path, submodule):
#     with open(dgit_path, "w") as f:
#         json.dump({"submodule": submodule}, f, indent=4, sort_keys=True)

def dgit_init():
    # git init
    if not os.path.isdir(".git"):
        com = "git init -b main"
        command_run(command=com)
    else:
        print("git existed.")

    # dvc init
    if not os.path.isdir(".dvc"):
        com = "dvc init"
        command_run(command=com)
    else:
        print("dvc existed.")

    print("\nSetting remote storage if not set yet.")
    print("\t$ dgit remote_add -h")


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "Init the git and dgit"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "init",
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
        dgit_init()
        # print(args.w)
