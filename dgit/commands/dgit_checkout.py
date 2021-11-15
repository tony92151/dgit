import argparse
import os
import git
from git import Repo
from .utils import command_run, DGIT_DATA_FILE, check_git_path


def dgit_checkout(dvc_path, repo: Repo, selected_tag,args, unknowargs: list):
    # print("")
    # repo.pull()
    # com = "git pull".format(dvc_path)
    # command_run(command=com)
    try:
        repo.git.checkout(selected_tag)
    except git.exc.GitCommandError:
        print("tag not match.")
        exit(1)

    if args.without_data:
        pass
    else:
        com = "dvc --cd {} pull {}".format(dvc_path, DGIT_DATA_FILE)
        command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "Checkout to specific version."
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "checkout",
            help=self.command_help,
        )

        self.parser.add_argument(
            '--list-tags',
            help='list all tags and select.',
            action='store_true'
        )

        self.parser.add_argument(
            '--without-data',
            help='pull {} only'.format(DGIT_DATA_FILE),
            action='store_true'
        )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        print(unknownargs)
        check_git_path()
        if len(unknownargs) < 1:
            self.parser.print_help()

        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        repo = Repo(path=dvc_path)

        if args.list_tags:
            for i, v in enumerate(repo.tags):
                print("({}) {}".format(i, v))

            selected_tag = str(repo.tags[int(input("? "))])
        else:
            selected_tag = unknownargs[0]

        dgit_checkout(dvc_path,
                      repo,
                      selected_tag,
                      args,
                      unknownargs)

