import argparse
import os
import subprocess

from .utils import command_run


# dvc add --no-commit

def run_dvc_commit(dvc_path, args, unknowargs: list):
    # print("")
    # dvc commit
    com = "dvc --cd {} commit ".format(dvc_path)
    for a in unknowargs:
        com += "{} ".format(a)
    command_run(command=com)

    # git commit
    com = "git commit -m '{}'".format(args.m)
    # for a in unknowargs:
    #     com += "{} ".format(a)
    command_run(command=com)

    # git tag
    if args.force:
        # remove tag on remote(github)
        # git push origin :v1_data

        com = "git push origin :{} && git tag -d {} && git tag {} -a -m 'add tag {}'".format(
            args.tag, args.tag, args.tag, args.tag)
    else:
        com = "git tag {} -a -m 'add tag {}'".format(args.tag, args.tag)
    # for a in unknowargs:
    #     com += "{} ".format(a)
    command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "dvc commit [args]"
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
            help='tag to this commit.',
            required=True,
        )

        self.parser.add_argument(
            '--force',
            action="store_true",
            help='Replace existed tag.',
        )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        print(unknownargs)
        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        run_dvc_commit(dvc_path,
                       args,
                       unknownargs)
        # from git import Repo
        # repo = Repo(path=os.path.join(".", dgit_read(os.path.join(".", ".dgit"))["submodule"]))
        # if args.tags:
        #     for i, v in enumerate(repo.tags):
        #         print("({}) {}".format(i, v))
