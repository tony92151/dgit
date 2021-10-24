import argparse
import os
import subprocess

from .utils import command_run


# dvc add --no-commit

def dgit_remote_add(dvc_path, args, unknownargs=None):
    # dgit remote add
    com = "dvc remote add -d --local {} {}".format(args.name, args.url)

    # add unknownargs
    for a in unknownargs:
        com += "{} ".format(a)

    print("\n $ {}".format(com))
    print("\n")
    command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "dvc remote add -d --local [args] s3://[args]"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "add",
            help=self.command_help,
        )

        self.parser.add_argument(
            '--name',
            type=str,
            default="myremote",
            help='name for remote storage, exp: myremote',
            required=True
        )

        self.parser.add_argument(
            '--url',
            type=str,
            default="s3://mybucket",
            help='bucket on remote storage, exp: s3://mybucket',
            required=True
        )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        print(unknownargs)
        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        dgit_remote_add(dvc_path,
                        args,
                        unknownargs)
        # from git import Repo
        # repo = Repo(path=os.path.join(".", dgit_read(os.path.join(".", ".dgit"))["submodule"]))
        # if args.tags:
        #     for i, v in enumerate(repo.tags):
        #         print("({}) {}".format(i, v))
