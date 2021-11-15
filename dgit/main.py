import argparse
import json
import os
import git

from .commands import dgit_init, dgit_checkout, dgit_data_pull, dgit_add, dgit_commit, dgit_pull, dgit_remote, \
    dgit_git, dgit_push

from .commands.utils import check_git_path
# from dgit.commands import dgit_init

COMMANDS = [
    dgit_init,
    dgit_checkout,
    # dgit_data_pull,
    dgit_add,
    dgit_commit,
    dgit_pull,
    dgit_push,
    dgit_remote,
    # dgit_git
]


# if __name__ == "__main__":
def main():
    parent_parser = argparse.ArgumentParser("dgit")

    # Sub commands
    subparsers = parent_parser.add_subparsers(title="Available Commands")

    # cmd_init = dgit_init.CMD_init(subparsers)
    # cmd_check = dgit_check.CMD_init(subparsers)

    # check git repo
    try:
        repo = git.Repo(".")
    except git.exc.InvalidGitRepositoryError:
        print("Not in a git repository.")

    # check git submudule whether dgit project

    dgit_submudule = []
    for s in repo.submodules:
        if os.path.isdir(os.path.join(s.abspath, ".dgit")):
            dgit_submudule.append(s.abspath)

    if len(dgit_submudule) > 1:
        print("Multi dgit repository found in submudule. Please enter submudule to operate.")
    elif len(dgit_submudule) == 1:
        get_submudule = dgit_submudule[0].abspath

        print("Find submodule: {}".format(get_submudule))
        os.environ["DVC_REPO_PATH"] = get_submudule
    elif os.path.isdir(os.path.join(".", ".dgit")):
        pass
    else:
        check_git_path()

    cmd = [c.CMD_init(subparsers) for c in COMMANDS]

    args, unknownargs = parent_parser.parse_known_args()

    try:
        args.func(args, unknownargs)
    except AttributeError:
        parent_parser.print_help()
