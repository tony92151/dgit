import argparse
import os
import subprocess
import json
from .utils import command_run, locate_dgit_path


# import .dgit_remote_add


def dgit_remote_add(dgit_path, args, unknownargs=None):
    # dgit remote add
    com = "dvc --cd {} remote add -d {} {}".format(dgit_path, args.name, args.url)

    # add unknownargs
    for a in unknownargs:
        com += "{} ".format(a)
    command_run(command=com)

    # dgit remote modify
    if args.endpointurl is not None:
        com = "dvc --cd {} remote modify {} endpointurl {}".format(dgit_path, args.name, args.endpointurl)

        # add unknownargs
        for a in unknownargs:
            com += "{} ".format(a)
        command_run(command=com)

    if args.git_commit:
        com = "git add .dvc && git commit -m \"dvc init\""
        command_run(command=com)
    else:
        print("\nRemind: you can make a checkpoint for dvc setting before data versioning.")
        print("\t$ git add .dvc && git commit -m \"dvc init\"")

    if args.s3_key is not None:
        if len(args.s3_key.split(":")) == 2:
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = args.s3_key.split(":")
            key = {"AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
                   "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY}
            with open(os.join(locate_dgit_path(), ".dgit", "key.key"), "r") as f:
                json.dump(key, f, indent=4, sort_keys=True)
        else:
            print("Error s3 key format.")


class CMD_init:
    def __init__(self, subparsers):
        # self.command_help = "dvc remote add -f -d --local [args] s3://[args] && dvc remote modify [args] [args]"
        self.command_help = "Specific remote s3 storage."
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "remote_add",
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

        self.parser.add_argument(
            '--s3-key',
            type=str,
            default=None,
            help='save s3 key in the repo. exp: AWS_ACCESS_KEY_ID:AWS_SECRET_ACCESS_KEY',
        )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        dgit_path = locate_dgit_path()
        dgit_remote_add(dgit_path,
                        args,
                        unknownargs)
