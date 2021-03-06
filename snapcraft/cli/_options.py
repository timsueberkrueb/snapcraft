# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2016 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import click

from snapcraft import ProjectOptions


class OptionWithHidden(click.Option):

    def __init__(self, *args, **kwargs):
        self.hidden = kwargs.pop('hidden', False)
        super().__init__(*args, **kwargs)

    def get_help_record(self, ctx):
        if self.hidden:
            return
        super().get_help_record(ctx)


_BUILD_OPTION_NAMES = [
    '--enable-geoip',
    '--no-parallel-builds',
    '--target-arch',
]

_BUILD_OPTIONS = [
    dict(is_flag=True,
         help=('Detect best candidate location for stage-packages using '
               'geoip')),
    dict(is_flag=True,
         help='Force a squential build.'),
    dict(metavar='<arch>',
         help='Target architecture to cross compile to'),
]


def add_build_options(hidden=False):
    def _add_build_options(func):
        for name, params in zip(reversed(_BUILD_OPTION_NAMES),
                                reversed(_BUILD_OPTIONS)):
            option = click.option(name, **params,
                                  cls=OptionWithHidden, hidden=hidden)
            func = option(func)
        return func
    return _add_build_options


def get_project_options(**kwargs):
    project_args = dict(
        use_geoip=kwargs.pop('enable_geoip'),
        parallel_builds=not kwargs.pop('no_parallel_builds'),
        target_deb_arch=kwargs.pop('target_arch'),
    )

    return ProjectOptions(**project_args)
