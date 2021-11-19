import argparse
import json
import os
import git

from .commands import dgit_init, dgit_checkout, dgit_data_pull, dgit_add, dgit_commit, dgit_pull, dgit_remote, \
    dgit_git, dgit_push, dgit_tag

from .commands.utils import locate_dgit_path, locate_git_path
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
    dgit_tag,
]


# if __name__ == "__main__":
def main():
    parent_parser = argparse.ArgumentParser("dgit")

    # Sub commands
    subparsers = parent_parser.add_subparsers(title="Available Commands")

    # cmd_init = dgit_init.CMD_init(subparsers)
    # cmd_check = dgit_check.CMD_init(subparsers)

    # check git repo
    # dgit_submodule = []
    # try:
    #     repo = git.Repo(".")
    #     # check git submodule whether dgit project
    #     for s in repo.submodules:
    #         if os.path.isdir(os.path.join(s.abspath, ".dgit")):
    #             dgit_submodule.append(s.abspath)
    # except git.exc.InvalidGitRepositoryError:
    #     print("Not in a git repository.")
    #     exit(1)
    #
    # if len(dgit_submodule) > 1:
    #     print("Multi dgit repository found in submodule. Please enter submodule to operate.")
    #     exit(1)
    # elif len(dgit_submodule) == 1:
    #     get_submudule = dgit_submodule[0].abspath
    #     print("Find submodule: {}".format(get_submudule))
    #     os.environ["DVC_REPO_PATH"] = get_submudule

    cmd = [c.CMD_init(subparsers) for c in COMMANDS]

    args, unknownargs = parent_parser.parse_known_args()

    try:
        args.func(args, unknownargs)
    except AttributeError:
        parent_parser.print_help()
