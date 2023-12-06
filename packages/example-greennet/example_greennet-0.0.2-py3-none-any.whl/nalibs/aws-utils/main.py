#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
from subprocess import run, PIPE, DEVNULL
from utils_secrets_manager import get_secret

LOG: logging.Logger


def get_version() -> str:
    """Obtain version information from git if available otherwise use
    the internal version number
    """

    def internal_version():
        return ".".join(map(str, __version_info__[:3])) + "".join(__version_info__[3:])

    return internal_version()
    # try:
    #     p = run(["git", "describe", "--tags"], stdout=PIPE, stderr=DEVNULL, text=True)
    # except FileNotFoundError:
    #     return internal_version()

    # if p.returncode:
    #     return internal_version()
    # else:
    #     return p.stdout.strip()


__version_info__ = (1, 1, 0, "+aws-utils")
__version__: str = get_version()


class NotFoundError(Exception):
    """Exception to handle situations where a credentials file is not found"""

    pass


class Exit(Exception):
    """Exception to allow a clean exit from any point in execution"""

    CLEAN = 0
    ERROR = 1
    MISSING_PROFILEINI = 2
    MISSING_SECRETS = 3
    BAD_PROFILEINI = 4
    LOCATION_NO_DIRECTORY = 5
    BAD_SECRETS = 6
    BAD_LOCALE = 7

    FAIL_LOCATE_NSS = 10
    FAIL_LOAD_NSS = 11
    FAIL_INIT_NSS = 12
    FAIL_NSS_KEYSLOT = 13
    FAIL_SHUTDOWN_NSS = 14
    BAD_PRIMARY_PASSWORD = 15
    NEED_PRIMARY_PASSWORD = 16
    DECRYPTION_FAILED = 17

    PASSSTORE_NOT_INIT = 20
    PASSSTORE_MISSING = 21
    PASSSTORE_ERROR = 22

    READ_GOT_EOF = 30
    MISSING_CHOICE = 31
    NO_SUCH_PROFILE = 32

    UNKNOWN_ERROR = 100
    KEYBOARD_INTERRUPT = 102

    def __init__(self, exitcode):
        self.exitcode = exitcode

    def __unicode__(self):
        return f"Premature program exit with exit code {self.exitcode}"


def parse_sys_args() -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description="nalibs - tiny tools"
    )

    parser.add_argument(
        "--secret-name",
        action="store",
        help="AWS Secret Name",
    )
    parser.add_argument(
        "-r",
        "--region",
        action="store",
        default="ap-southeast-1",
        help="AWS Region",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity level. Warning on -vv (highest level) user input will be printed on screen",
    )
    # parser.add_argument(
    #     "--version",
    #     action="version",
    #     version=__version__,
    #     help="Display version of firefox_decrypt and exit",
    # )

    args = parser.parse_args()

    return args


def setup_logging(args) -> None:
    """Setup the logging level and configure the basic logger"""
    if args.verbose == 1:
        level = logging.INFO
    elif args.verbose >= 2:
        level = logging.DEBUG
    else:
        level = logging.WARN

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=level,
    )

    global LOG
    LOG = logging.getLogger(__name__)


def main() -> None:
    """Main entry point"""
    args = parse_sys_args()

    setup_logging(args)

    LOG.info("Running version: %s", __version__)
    LOG.debug("Parsed commandline arguments: %s", args)
    
    ## Get Secrets
    LOG.info(get_secret("example", "ap-southeast-1"))


def run():
    try:
        main()
    except KeyboardInterrupt:
        print("Quit.")
        sys.exit(Exit.KEYBOARD_INTERRUPT)
    except Exit as e:
        sys.exit(e.exitcode)


if __name__ == "__main__":
    run()
