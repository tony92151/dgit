import argparse


class CMD_init:
    def __init__(self, subparsers):
        self.command_help = "check the dgit in .dgit"
        self.parser = None
        self.add_parser(subparsers)

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(
            "check",
            help=self.command_help,
        )

        self.parser.add_argument('-a',
                                 type=int,
                                 default=1,
                                 help="a"
                                 )

        self.parser.add_argument('-b',
                                 type=int,
                                 default=2,
                                 help="b"
                                 )

        self.parser.set_defaults(func=self.command)

    def command(self, args, unknownargs):
        print(args.a + args.b)
