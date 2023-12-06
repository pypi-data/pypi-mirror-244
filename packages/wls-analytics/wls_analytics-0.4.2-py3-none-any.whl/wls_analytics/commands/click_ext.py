# -*- coding: utf-8 -*-
# @author: Tomas Vitvar, https://vitvar.com, tomas.vitvar@oracle.com

import json
import os
import re
import sys
import time
import sys
import signal
import typing as t

import click
import traceback
import logging

from click.core import Command

from .. import config

from wls_analytics import __version__ as version
from ..config import init_logging
from ..utils import format_str_color, bcolors
from ..utils import import_class

from typing import Any, Dict, Sequence
from click import Option

from datetime import datetime, timedelta


def get_set_reader(config, set_name):
    logs_set = config(f"sets.{set_name}")
    cls_name = config(f"sets.{set_name}.reader")
    reader_class = import_class(cls_name, raise_ex=False)
    if reader_class is None:
        raise Exception(f"The reader class '{cls_name}' for the set '{set_name}' cannot be imported!")
    if logs_set is None:
        raise Exception(f"The log set '{set_name}' not found in the configuration file.")
    return logs_set, reader_class


def get_time_range(time_from, time_to, offset):
    if time_from is None and time_to is None:
        raise Exception("Either --from or --to must be specified.")
    if time_to is None:
        time_to = datetime.now()
    if time_from is None and offset is not None:
        time_from = time_to - offset
    return time_from, time_to


class DateTimeOption(click.Option):
    def type_cast_value(self, ctx, value):
        if value is None:
            return None
        for fmt in ["%Y-%m-%d %H:%M:%S", "%H:%M:%S", "%H:%M"]:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass
        raise click.BadParameter("use values in the format '%Y-%m-%d %H:%M:%S', '%H:%M:%S' or '%H:%M'.")


class OffsetOption(click.Option):
    def type_cast_value(self, ctx, value):
        if value is None:
            return None
        offset_units = {"h": "hours", "d": "days", "m": "minutes"}
        unit = value[-1]
        if unit in offset_units:
            try:
                value = int(value[:-1])
                return timedelta(**{offset_units[unit]: value})
            except ValueError:
                pass
        raise click.BadParameter("use values like '1h', '2d', '10m'.")


class CoreCommandGroup(click.core.Group):
    """
    The `CoreCommand` is the main entry point for the CLI. It initializes the global variables and
    the logger, and handles the global options such as `--no-ansi` and `--debug`.
    """

    def invoke(self, ctx):
        """
        The main method to run the command.
        """
        # retrieve the global options
        config.ANSI_COLORS = not ctx.params.pop("no_ansi", config.ANSI_COLORS)
        config.YAMC_DEBUG = ctx.params.pop("debug")
        config.TRACEBACK = ctx.params.pop("traceback", config.TRACEBACK)

        # pylint: disable=broad-except
        try:
            # for sig in ("TERM", "INT"):
            #     signal.signal(
            #         getattr(signal, "SIG" + sig),
            #         lambda x, y: config.exit_event.set(),
            #     )
            click.core.Group.invoke(self, ctx)
        except click.exceptions.Exit as exception:
            sys.exit(int(str(exception)))
        except click.core.ClickException as exception:
            raise exception
        except Exception as exception:
            sys.stderr.write(
                format_str_color(
                    f"ERROR: {str(exception)}\n",
                    bcolors.ERROR,
                    not config.ANSI_COLORS,
                )
            )
            if config.TRACEBACK:
                print("---")
                traceback.print_exc()
                print("---")

            sys.exit(1)


class BaseCommand(click.core.Command):
    """
    The `BaseCommand` is the base class for all commands. It initializes the logger.
    """

    def __init__(self, *args, **kwargs):
        if kwargs.get("log_handlers"):
            self.log_handlers = kwargs.get("log_handlers")
            kwargs.pop("log_handlers")
        else:
            # default log handlers
            self.log_handlers = ["file", "console"]
        super().__init__(*args, **kwargs)

    def init_logging(self, command_path):
        logs_dir = os.path.join(config.WLSA_HOME, "logs", "-".join(command_path.split(" ")[1:]))
        os.makedirs(logs_dir, exist_ok=True)
        filename_suffix = "-".join(command_path.split(" ")[1:])
        init_logging(
            logs_dir,
            filename_suffix,
            handlers=self.log_handlers,
        )

    def command_run(self, ctx):
        self.init_logging(ctx.command_path)
        self.log = config.get_logger(ctx.command.name)
        self.log.info(f"WebLogic Analytics, wls-analytics v{version}")

    def invoke(self, ctx):
        self.command_run(ctx)
        return super().invoke(ctx)


class BaseCommandConfig(BaseCommand):
    """
    The `BaseCommandConfig` is the base class for all commands that require the configuration file.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.insert(
            0,
            Option(
                ("-c", "--config"),
                metavar="<file>",
                required=True,
                help="Configuration file",
                default=config.CONFIG_FILE,
            ),
        )
        self.log = None

    def command_run(self, ctx):
        super().command_run(ctx)
        config_file = ctx.params.pop("config")
        _config = config.Config(config_file)
        self.log.info(f"The configuration loaded from {_config.config_file}")
        ctx.params["config"] = _config
        ctx.params["log"] = self.log


# class TableCommand(BaseCommandConfig):
#     def __init__(self, *args, **kwargs):
#         self.table = Table(kwargs.pop("table_def", None), None, False)
#         self.watch_opts = kwargs.pop("watch_opts", [])
#         super().__init__(*args, **kwargs)
#         self.params.insert(
#             0,
#             Option(
#                 ("-d", "--describe"),
#                 help="Describe the table columns",
#                 is_flag=True,
#             ),
#         )
#         if "option" in self.watch_opts:
#             self.params.insert(
#                 0,
#                 Option(
#                     ("-w", "--watch"),
#                     help="Watch the data for changes and update the table.",
#                     is_flag=True,
#                 ),
#             )

#         self.describe = False
#         self.watch = False

#     def invoke(self, ctx):
#         self.describe = ctx.params.pop("describe")
#         self.watch = "always" in self.watch_opts or ctx.params.pop("watch", False)
#         if self.describe:
#             self.table.describe()
#         else:
#             data = super().invoke(ctx)
#             if isinstance(data, list):
#                 if not self.watch:
#                     self.table.display(data)
#                 else:
#                     self.table.watch(lambda: data)
#             elif callable(data):
#                 if self.watch:
#                     self.table.watch(data)
#                 else:
#                     self.table.display(data())
#             else:
#                 raise Exception("The data must be either a list or a callable object!")
