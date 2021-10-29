import argparse
import os
import subprocess

from .utils import command_run, DGIT_DATA_FILE


# dvc add --no-commit

def run_dvc_add(dvc_path, args, unknowargs: list):
    if not os.path.isfile(os.path.join(dvc_path, DGIT_DATA_FILE)):
        add_ignore = True
    else:
        add_ignore = False
    # print("")

    os.makedirs(os.path.dirname(os.path.join(dvc_path, DGIT_DATA_FILE)), exist_ok=True)
    com = "dvc --cd {} add --no-commit --file {} ".format(dvc_path, DGIT_DATA_FILE)
    for a in unknowargs:
        com += "{} ".format(a)

    command_run(command=com)

    # git add .dvc
    com = "git add {}".format(DGIT_DATA_FILE)
    # for a in unknowargs:
    #     com += "{}.dvc ".format(a)

    command_run(command=com)

    if add_ignore:
        com = "git add .gitignore"
        command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "dvc add --no-commit [args]"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "add",
            help=self.command_help,
        )

        # self.parser.add_argument(
        #     '--tags',
        #     help='list all tags',
        #     action='store_true'
        # )
        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        print(unknownargs)
        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        if len(unknownargs)<1:
            self.parser.print_help()
        run_dvc_add(dvc_path,
                    args,
                    unknownargs)
        # from git import Repo
        # repo = Repo(path=os.path.join(".", dgit_read(os.path.join(".", ".dgit"))["submodule"]))
        # if args.tags:
        #     for i, v in enumerate(repo.tags):
        #         print("({}) {}".format(i, v))
