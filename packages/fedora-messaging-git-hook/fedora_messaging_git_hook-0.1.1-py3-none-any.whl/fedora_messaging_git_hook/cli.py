# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys

import click
import pygit2
from fedora_messaging.config import conf

from .hook import process


@click.command()
@click.option("--config", help="Fedora Messaging configuration file")
def main(config):
    conf.load_config(config)
    hook_config = conf["consumer_config"]

    # Use $GIT_DIR to determine where this repo is.
    abspath = os.path.abspath(os.environ["GIT_DIR"])

    excluded_paths = hook_config.get("excluded_paths", [])
    if any([path in abspath for path in excluded_paths]):
        return

    repo = pygit2.Repository(abspath)
    # Read in all the rev information git-receive-pack hands us.
    click.echo("Emitting a message to the fedora-messaging message bus.")
    process(repo, hook_config, list(sys.stdin.readlines()))
