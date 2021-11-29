import argparse
import json
import os
import git

from .commands import \
    dgit_init, \
    dgit_checkout, \
    dgit_add, \
    dgit_commit, \
    dgit_pull, \
    dgit_remote, \
    dgit_push, \
    dgit_tag


COMMANDS = [
    dgit_init,
    dgit_checkout,
    dgit_add,
    dgit_commit,
    dgit_pull,
    dgit_push,
    dgit_remote,
    dgit_tag,
]


# if __name__ == "__main__":
def main():
    parent_parser = argparse.ArgumentParser("dgit")

    # Sub commands
    subparsers = parent_parser.add_subparsers(title="Available Commands")

    cmd = [c.CMD_init(subparsers) for c in COMMANDS]

    args, unknownargs = parent_parser.parse_known_args()

    try:
        args.func(args, unknownargs)
    except AttributeError:
        parent_parser.print_help()
