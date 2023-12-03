import argparse

from pcfl import __version__, pcfl_by_file


class _Parser:
    @property
    def root(self):
        parser = argparse.ArgumentParser(
            prog="pcfl",
            formatter_class=argparse.RawTextHelpFormatter,
            description="PCFL is Piano Compensator for FLstudio"
        )
        parser.add_argument("args", choices=["version", "run"])

        return parser

    @property
    def runner(self):
        parser = argparse.ArgumentParser(prog="pcfl run")
        parser.add_argument(
            "-f", "--file",
            type=str,
            required=True
        )
        parser.add_argument(
            "-o", "--output",
            type=str,
            required=False, default="result.mid",
        )
        return parser


class CommandLineInterface:
    parser = _Parser()
    def __call__(self):
        command, args = self.parser.root.parse_known_args()
        match command.args:
            case "version":
                print(f"v{__version__}")
            case "run":
                kwargs = self.parser.runner.parse_args(args)
                try:
                    pcfl_by_file(**kwargs.__dict__)
                except Exception as e:
                    print(f"[ERROR]: {str(e)}")