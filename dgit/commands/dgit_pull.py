import argparse
import os
import subprocess
from git import Repo
from .utils import command_run, DGIT_DATA_FILE


# dvc add --no-commit

def check_s3_key():
    if os.getenv("AWS_ACCESS_KEY_ID", None) is None:
        os.environ["AWS_ACCESS_KEY_ID"] = input("AWS_ACCESS_KEY_ID=")

    if os.getenv("AWS_SECRET_ACCESS_KEY", None) is None:
        os.environ["AWS_SECRET_ACCESS_KEY"] = input("AWS_SECRET_ACCESS_KEY=")


def dgit_pull(dvc_path, repo: Repo, args, unknowargs: list):
    # print("")
    repo.pull()
    # com = "git pull".format(dvc_path)
    # command_run(command=com)

    if args.without_data:
        pass
    # if args.data:
    #     for i, v in enumerate(repo.tags):
    #         print("({}) {}".format(i, v))
    #
    #     selected_tag = str(repo.tags[int(input("? "))])
    #     repo.git.checkout(selected_tag, os.path.join("AI9_data_version.dvc"))
    #     print("\ngit checkout to : ", selected_tag)
    #
    #     print("\nCheck s3 key...")
    #     check_s3_key()
    #     com = "dvc --cd {} pull".format(dvc_path)
    #     command_run(command=com)


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "dvc pull [args]"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "pull",
            help=self.command_help,
        )

        self.parser.add_argument(
            '--without-data',
            help='pull {} only'.format(DGIT_DATA_FILE),
            action='store_true'
        )
        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        print(unknownargs)
        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        repo = Repo(path=dvc_path)

        dvc_path = os.getenv("DVC_REPO_PATH", ".")
        dgit_pull(dvc_path,
                  repo,
                  args,
                  unknownargs)
        # from git import Repo
        # repo = Repo(path=os.path.join(".", dgit_read(os.path.join(".", ".dgit"))["submodule"]))
        # if args.tags:
        #     for i, v in enumerate(repo.tags):
        #         print("({}) {}".format(i, v))
