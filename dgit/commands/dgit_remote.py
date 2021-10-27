import argparse
import os
import subprocess

from .utils import command_run
# import .dgit_remote_add
from . import dgit_remote_add, dgit_remote_modify


# dvc add --no-commit

def dgit_remote_add(dvc_path, args, unknownargs=None):
    # dgit remote add
    com = "dvc --cd {} remote add -d {} {}".format(dvc_path, args.name, args.url)

    # add unknownargs
    for a in unknownargs:
        com += "{} ".format(a)
    command_run(command=com)

    # dgit remote modify
    if args.endpointurl is not None:
        com = "dvc --cd {} remote modify {} endpointurl {}".format(dvc_path, args.name, args.endpointurl)

        # add unknownargs
        for a in unknownargs:
            com += "{} ".format(a)
        command_run(command=com)

    print(args)
    if args.git_commit:
        com = "git add .dvc && git commit -m \"dvc init\""
        command_run(command=com)
    else:
        print("\nRemind: you can make a checkpoint for dvc setting before data versioning.")
        print("\t$ git add .dvc && git commit -m \"dvc init\"")


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "dvc remote add -f -d --local [args] s3://[args] && dvc remote modify [args] [args]"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "remote_add",
            help=self.command_help,
        )

        # self.parser.

        # _ = dgit_remote_add(self.parser)
        # _ = dgit_remote_modify(self.parser)

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

        self.parser.add_argument(
            '--endpointurl',
            type=str,
            default=None,
            help='endpointurl to remote s3 provider, exp: https://myendpoint.com',
        )

        self.parser.add_argument(
            '--git-commit',
            action="store_true",
            help='make a checkpoint for dvc setting before data versioning $ git add .dvc && git commit -m \"dvc init\"',
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
