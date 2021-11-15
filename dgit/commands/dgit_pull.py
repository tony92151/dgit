import argparse
import os
import subprocess
from git import Repo
from .utils import command_run, DGIT_DATA_FILE, check_git_path


# dvc add --no-commit

def check_s3_key():
    if os.getenv("AWS_ACCESS_KEY_ID", None) is None:
        os.environ["AWS_ACCESS_KEY_ID"] = input("AWS_ACCESS_KEY_ID=")

    if os.getenv("AWS_SECRET_ACCESS_KEY", None) is None:
        os.environ["AWS_SECRET_ACCESS_KEY"] = input("AWS_SECRET_ACCESS_KEY=")


def dgit_pull(dvc_path, repo: Repo, args, unknowargs: list):
    # print("")
    o = repo.remotes.origin
    o.pull()

    # if args.without_data:
    #     pass
    # else:
    #     com = "dvc --cd {} pull {}".format(dvc_path, DGIT_DATA_FILE)
    #     command_run(command=com)
    com = "dvc --cd {} pull {}".format(dvc_path, DGIT_DATA_FILE)
    command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "Incorporates changes from a remote repository into the current branch and pull newest data from remote storage."
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "pull",
            help=self.command_help,
        )

        # self.parser.add_argument(
        #     '--without-data',
        #     help='Pull git repository only.',
        #     action='store_true'
        # )

        # self.parser.add_argument(
        #     '--force',
        #     help='',
        #     action='store_true'
        # )


        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        print(unknownargs)
        check_git_path()
        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        repo = Repo(path=dvc_path)

        check_s3_key()

        #dvc_path = os.getenv("DVC_REPO_PATH", ".")
        dgit_pull(dvc_path,
                  repo,
                  args,
                  unknownargs)
        # from git import Repo
        # repo = Repo(path=os.path.join(".", dgit_read(os.path.join(".", ".dgit"))["submodule"]))
        # if args.tags:
        #     for i, v in enumerate(repo.tags):
        #         print("({}) {}".format(i, v))
