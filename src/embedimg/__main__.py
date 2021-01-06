#!/usr/bin/env python


import sys
from embedimg import version
from embedimg import entry


def embedimg():
    sys.exit(entry.cli_start(version.version))


if __name__ == "__main__":
    embedimg()
