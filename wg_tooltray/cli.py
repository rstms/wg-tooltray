"""Console script for firefox_exec."""


import sys
import time
import json

from time import sleep
from pathlib import Path

import click

from .exception_handler import ExceptionHandler
from .version import __timestamp__, __version__
from .tray_icon import TrayIcon

DEFAULT_CONFIG=Path.home()/'.wgtt.json'

header = f"{__name__.split('.')[0]} v{__version__} {__timestamp__}"

@click.command("wg-tooltray")
@click.version_option(message=header)
@click.option("-d", "--debug", is_flag=True, help="debug mode")
@click.option("-c", "--config", type=click.Path(dir_okay=False, readable=True, path_type=Path), default=DEFAULT_CONFIG, help="config file")
@click.pass_context
def cli(ctx, debug, config):

    ctx.obj = dict(ehandler=ExceptionHandler(debug))

    networks=json.loads(config.read_text())

    with TrayIcon("Wireguard VPN", networks=networks) as icon:
        while(True):
            sleep(60)

if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
