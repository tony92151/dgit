import argparse
import json
import os
import git

from .commands import dgit_init, dgit_checkout, dgit_data_pull, dgit_add, dgit_commit, dgit_pull, dgit_remote, \
    dgit_git, dgit_push

# from dgit.commands import dgit_init

COMMANDS = [
    dgit_init,
    dgit_check,
    dgit_data_pull,
    dgit_add,
    dgit_commit,
    dgit_pull,
    dgit_push,
    dgit_remote,
    dgit_git
]


# if __name__ == "__main__":
def main():
    parent_parser = argparse.ArgumentParser("dgit")

    # Sub commands
    subparsers = parent_parser.add_subparsers(title="Available Commands")

    # cmd_init = dgit_init.CMD_init(subparsers)
    # cmd_check = dgit_check.CMD_init(subparsers)


    try:
        repo = git.Repo(".")
        get_submudule = repo.submodules[0].abspath
        os.environ["DVC_REPO_PATH"] = get_submudule
        print("Find submodule: {}".format(get_submudule))
    except:
        pass

    cmd = [c.CMD_init(subparsers) for c in COMMANDS]

    args, unknownargs = parent_parser.parse_known_args()

    try:
        args.func(args, unknownargs)
    except AttributeError:
        parent_parser.print_help()
