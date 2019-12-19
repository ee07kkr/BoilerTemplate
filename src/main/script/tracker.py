#! /usr/bin/env python3
import sys
import os
import logging
from traceback import format_exc
from argparse import ArgumentParser
from reporting.report import who_in_space

logging.basicConfig(filename='profusion.log', level=logging.INFO)

def main(argv=None):
    """
    Main function that calls who_in_space function.
    """
    program_name = os.path.basename(sys.argv[0])
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    try:
        parser = ArgumentParser(description='Parse the link for api')

        parser.add_argument('apilink', help='Api link with info on whos in space', nargs = '*',type=str, default='http://api.open-notify.org/astros.json')

        args = parser.parse_args()
        logging.info("Beginning parse api and see who is in space!")
        who_in_space(args.apilink)
        logging.info("Done, look at csv for tabular info of who in space")
        return 0

    except Exception as e:
        sys.stderr.write(program_name + ": " + repr(e) + '\n' + format_exc() + '\n')
        raise e


if __name__ == "__main__":
    sys.exit(main())
