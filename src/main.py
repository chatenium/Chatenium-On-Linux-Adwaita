# main.py
#
# Copyright 2025 Parallels
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi
import asyncio

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import MainWindow
import os

class ChateniumadwApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='hu.chatenium.chtnoladw',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/hu/chatenium/chtnoladw')

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()


def main(version):
    """The application's entry point."""
    app = ChateniumadwApplication()

    return app.run(sys.argv)
