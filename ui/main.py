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
import math
import time
import string
import datetime
import gobject
import gtk
import wnck
import sqlite3

from standards.xdg import BaseDir

import i18n
_ = i18n.init()


class StatisticsWindow(gtk.Window):

    COLUMN_APPLICATION = 0
    COLUMN_SECONDS = 1
    COLUMN_PERCENTAGE = 2

    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

        self.set_title('Application Time Tracker')
        self.set_icon_name('application-x-executable')
        self.set_default_size(500, 400)
        self.set_position(gtk.WIN_POS_CENTER)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(scrolled_window)
        scrolled_window.show()

        self.store = gtk.ListStore(gobject.TYPE_STRING, \
                gobject.TYPE_UINT64, gobject.TYPE_FLOAT)
        self.store.set_sort_column_id(self.COLUMN_PERCENTAGE, gtk.SORT_DESCENDING)

        tree_view = gtk.TreeView(self.store)
        tree_view.set_headers_visible(True)
        scrolled_window.add(tree_view)
        tree_view.show()

        column = gtk.TreeViewColumn(_('Application'))
        renderer = gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', self.COLUMN_APPLICATION)
        column.set_property('expand', True)
        tree_view.append_column(column)

        column = gtk.TreeViewColumn(_('Seconds Used'))
        renderer = gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', self.COLUMN_SECONDS)
        column.set_cell_data_func(renderer, self.set_seconds)
        tree_view.append_column(column)

        column = gtk.TreeViewColumn(_('Percentage'))
        renderer = gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', self.COLUMN_SECONDS)
        column.set_cell_data_func(renderer, self.set_percentage)
        tree_view.append_column(column)

    def update_statistics(self, database):
        self.store.clear()
        
        usages = database.get_usages()

        stats = {}
        total_seconds = 0

        for row in usages:
            if row['name'] in stats:
                timespan = (row['endtime'] - row['starttime']).seconds
                stats[row['name']] += timespan
            else:
                timespan = (row['endtime'] - row['starttime']).seconds
                stats[row['name']] = timespan

            total_seconds += timespan

        for key in stats:
            percentage = float(stats[key]) / float(total_seconds)

            iter = self.store.append()
            self.store.set(iter, \
                    self.COLUMN_APPLICATION, key,
                    self.COLUMN_SECONDS, stats[key],
                    self.COLUMN_PERCENTAGE, percentage)

    def set_seconds(self, column, renderer, model, iter):
        seconds = model.get_value(iter, self.COLUMN_SECONDS)
        renderer.set_property('text', str(seconds))

    def set_percentage(self, column, renderer, model, iter):
        percentage = model.get_value(iter, self.COLUMN_PERCENTAGE)
        renderer.set_property('text', '%3.2f %%' % (percentage * 100))


class StatusIcon(gtk.StatusIcon):

    def __init__(self):
        gtk.StatusIcon.__init__(self)

        self.set_from_icon_name('application-x-executable')


class Database(gobject.GObject):

    def __init__(self):
        gobject.GObject.__init__(self)

        self.open_database()
        self.initialize_database()

    def open_database(self):
        # build the database filename
        filename = os.path.join(BaseDir.get_config_home(), \
            'app-time-tracker', 'database.sqlite')

        if not os.path.isdir(os.path.dirname(filename)):
            # create the config directory if necessary
            os.makedirs(os.path.dirname(filename))

        # open the database
        self.db = sqlite3.connect(filename, \
                detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.db.row_factory = sqlite3.Row

    def initialize_database(self):
        cursor = self.db.cursor()
        
        try:
            cursor.execute('''
                create table applications (
                    id integer primary key,
                    name text unique
                )''')
        except:
            pass

        try:
            cursor.execute('''
                create table usage (
                    application_id integer,
                    starttime timestamp,
                    endtime timestamp
                )''')
        except:
            pass

        # commit the changes made to the database
        self.db.commit()
            

    def store_event(self, application, start_time, end_time):
        start_date = datetime.datetime.fromtimestamp(start_time)
        end_date = datetime.datetime.fromtimestamp(end_time)

        cursor = self.db.cursor()
        
        cursor.execute('select * from applications where name=?', (application,))
        result = cursor.fetchone()

        if result:
            id = result['id']
        else:
            cursor.execute('insert into applications(name) values (?)', (application,))
            id = cursor.lastrowid

        if end_date.date() > start_date.date():
            start_midnight = start_date.replace(start_date.year, start_date.month, \
                    start_date.day, 23, 59, 59, 999999)

            end_midnight = start_date.replace(start_date.year, start_date.month, \
                    start_date.day + 1, 0, 0, 0, 0)

            cursor.execute('insert into usage values (?,?,?)', \
                    (id, start_date, start_midnight))

            cursor.execute('insert into usage values (?,?,?)', \
                    (id, end_midnight, end_date))
        else:
            cursor.execute('insert into usage values (?,?,?)', \
                    (id, start_date, end_date))
            
        # commit the changes made to the database
        self.db.commit()

    def get_applications(self):
        cursor = self.db.cursor()
        cursor.execute('select * from applications')
        return cursor.fetchall()

    def get_usages(self):
        cursor = self.db.cursor()
        cursor.execute('select * from usage inner join applications where application_id=id')
        return cursor.fetchall()


class WindowTracker(gobject.GObject):

    def __init__(self):
        gobject.GObject.__init__(self)

        # determine default screen 
        screen = wnck.screen_get_default()

        # determine the current time and active window
        self.old_time = time.time()
        self.old_window = screen.get_active_window()

        # be notified when the active window changes
        screen.connect('active-window-changed', self.active_window_changed)

    def active_window_changed(self, screen, previous_window):
        old_window = self.old_window
        old_time = self.old_time

        new_time = time.time()
        new_window = screen.get_active_window()

        old_app = None

        if old_window:
            application = old_window.get_application()
            if application:
                old_app = application.get_name()

        if old_app:
            old_app = string.strip(old_app)

        self.old_time = new_time
        self.old_window = new_window

        self.emit('application-changed', old_app, float(old_time), float(new_time))


gobject.type_register(WindowTracker)

gobject.signal_new('application-changed', WindowTracker, 
        gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
        (gobject.TYPE_STRING, gobject.TYPE_DOUBLE, gobject.TYPE_DOUBLE))


class AppTimeTrackerApplication(gobject.GObject):

    def __init__(self):
        # initialize the GLib threading system
        gtk.gdk.threads_init()

        # create the status icon
        self.status_icon = StatusIcon()
        self.status_icon.connect('activate', self.status_icon_activated)

        # create the statistics main window
        self.stats_window = StatisticsWindow()
        self.stats_window.hide()

        # create the window tracker
        self.window_tracker = WindowTracker()
        self.window_tracker.connect('application-changed', self.application_changed)

        # create the tracker database
        self.database = Database()

    def run(self):
        gtk.main()

    def application_changed(self, tracker, application, start_time, end_time):
        if application:
            self.database.store_event(application, start_time, end_time)
            self.stats_window.update_statistics(self.database)

    def status_icon_activated(self, status_icon):
        if self.stats_window.get_visible():
            self.stats_window.hide()
        else:
            self.stats_window.present()
