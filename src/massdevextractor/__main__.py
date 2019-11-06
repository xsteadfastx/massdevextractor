import logging
import sys

import structlog

from massdevextractor import cli


def entrypoint():
    cli.main()
