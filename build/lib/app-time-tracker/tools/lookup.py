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

import sys
from os import path


class Lookup:

    def __init__(self):
        # Build search paths list
        self.paths = set()
        self.paths.add(".")
        for path in sys.path:
            self.paths.add(path)

    def __call__(self):
        return self

    def icon(self, name):
        for dirname in self.paths:
            fullpath = path.join(dirname, "app-time-tracker", "data", "pixmaps", name)
            if path.isfile(fullpath):
                return fullpath
            
            fullpath = path.join(dirname, "data", "pixmaps", name)
            if path.isfile(fullpath):
                return fullpath

        return name

    def ui(self, name):
        for dirname in self.paths:
            fullpath = path.join(dirname, "app-time-tracker", "data", "ui", name)
            if path.isfile(fullpath):
                return fullpath

            fullpath = path.join(dirname, "data", "ui", name)
            if path.isfile(fullpath):
                return fullpath

        return name

    def data(self, file):
        for dirname in self.paths:
            fullpath = path.join(dirname, "app-time-tracker", "data", file)
            if path.isfile(fullpath):
                return fullpath

            fullpath = path.join(dirname, "data", file)
            if path.isfile(fullpath):
                return fullpath

        return file

    def locale(self):
        for dirname in self.paths:
            fullpath = path.join(dirname, "app-time-tracker", "i18n", "locale")
            if path.isdir(fullpath):
                return fullpath

            fullpath = path.join(dirname, "i18n", "locale")
            if path.isdir(fullpath):
                return fullpath

        return "locale"


Lookup = Lookup()

