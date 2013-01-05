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

from os import environ, path


class BaseDir:

    def __call__(self):
        return self

    def get_data_home(self):
        if self.isValid("XDG_DATA_HOME"):
            return environ.get("XDG_DATA_HOME")
        else:
            return path.join(self.getHome(), ".local", "share")

    def get_config_home(self):
        if self.isValid("XDG_CONFIG_HOME"):
            return environ.get("XDG_CONFIG_HOME")
        else:
            return path.join(self.getHome(), ".config")

    def get_data_dirs(self):
        if self.isValid("XDG_DATA_DIRS"):
            return environ.get("XDG_DATA_DIRS").split(":")
        else:
            return [path.join("usr", "local", "share"), \
                    path.join("usr", "share")]

    def get_config_dirs(self):
        if self.isValid("XDG_CONFIG_DIRS"):
            return environ.get("XDG_CONFIG_DIRS").split(":")
        else:
            return [path.join(self.getSysconfDir(), "xdg")]

    def get_home(self):
        if self.isValid("HOME"):
            return environ.get("HOME")
        else:
            return "~/"
    
    def get_path(self):
        return environ.get("PATH").split(":")

    def is_valid(self, key):
        return environ.has_key(key) and len(environ.get(key)) > 0

    def get_sysconf_dir(self):
        return "/etc" # TODO Do all posix-like platforms use this?


BaseDir = BaseDir()
