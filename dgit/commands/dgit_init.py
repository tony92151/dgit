import argparse
import json
import os


def dgit_init(dgit_path, submodule):
    with open(dgit_path, "w") as f:
        json.dump({"submodule": submodule}, f, indent=4, sort_keys=True)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "Init the dgit in .dgit"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "init",
            help=self.command_help,
        )
        self.parser.add_argument('--submodule',
                                 type=str,
                                 default=None,
                                 help="path to submodule",
                                 required=True
                                 )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        dgit_init(os.path.join(".", ".dgit"), args.submodule)
        # print(args.w)
