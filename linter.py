#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Wisdman
# Copyright (c) 2017 Wisdman <wisdman@ajaw.it>
#
# License: MIT
#

"""This module exports the TSLint2 plugin class."""

import os

from SublimeLinter.lint import NodeLinter, util


class TSLint2(NodeLinter):
    """Provides an interface to TSLint2."""

    syntax = ('typescript', 'typescriptreact')
    cmd = ('tslint', '@')
    npm_name = 'tslint'
    regex = (
        r'^.+?\[(?P<line>\d+), (?P<col>\d+)\]: '
        r'(?P<message>.+)'
    )
    error_stream = util.STREAM_BOTH
    config_file = ('--config', 'tslint.json', '~')
    tempfile_suffix = '-'
    version_args = '--version'
    version_requirement = '>= 5.0.0'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'

    def build_args(self, settings=None):
        """Override build_args to allow setting a custom config filename."""
        backup = self.config_file
        if 'config_filename' in settings and self.filename:
            self.config_file = self.config_file[:1] + (settings['config_filename'],) + self.config_file[2:]

        out = super().build_args(settings)

        projectPath = self.__findTSConfigPath()
        if projectPath is not None:
            out.extend(['--project', projectPath, '--type-check'])

        # Reset the value of config_file so that this can apply per-project.
        self.config_file = backup

        return out

    def __findTSConfigPath(self):
        return util.find_file(os.path.dirname(self.filename), 'tsconfig.json')

