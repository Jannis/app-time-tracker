#!/usr/bin/env python
#
# vi:set et ai sw=4 sts=4 ts=4: */
# -
# Copyright (c) 2010 Jannis Pohlmann <jannis@xfce.org>
# 
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of 
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public 
# License along with this program; if not, write to the Free 
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

import os
from sys import version_info, exit
from os import putenv
from commands import getstatusoutput
from distutils.core import setup
from distutils import sysconfig

import info
import i18n
_ = i18n.init()


def check_dependencies():
    # Check PyGTK dependency
    try:
        import pygtk
        pygtk.require("2.0")
        import gtk
        if gtk.pygtk_version < (2, 6, 0):
            raise ImportError
    except ImportError:
        print _("You need at least PyGTK 2.6 to run InstallIt (app-time-tracker)")
        exit(1)


# Check if required dependencies are available
check_dependencies()


# Setup information
setup(name = "app-time-tracker",
    version = info.version,
    description = _("Tracker for the time spent in applications"),
    long_description = _("Application Time Tracker (app-time-tracker) is a program to track the time spent in applications"),
    author = "Jannis Pohlmann",
    author_email = "jannis@xfce.org",
    url = "http://app-time-tracker.xfce.org",
    license = "GNU GPL",
    packages = [
        "app-time-tracker", 
        "app-time-tracker/standards", 
        "app-time-tracker/tools", 
        "app-time-tracker/i18n", 
        "app-time-tracker/ui",
    ],
    package_dir = {
        "app-time-tracker": ".",
        "app-time-tracker/standards": "standards",
        "app-time-tracker/tools": "tools",
        "app-time-tracker/i18n": "i18n",

        "app-time-tracker/ui": "ui",
    },
    package_data = { 
        "app-time-tracker": [
            "data/*.*", 
            "data/pixmaps/*.*",
            "data/ui/*.*",
            "i18n/locale/*/LC_MESSAGES/app-time-tracker.mo",
        ]
    },
    scripts = ["app-time-tracker"],
)
