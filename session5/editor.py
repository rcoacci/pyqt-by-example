# -*- coding: utf-8 -*-

"""A custom widget that edits a task's properties"""

# Import Qt modules
from PyQt4 import QtCore, QtGui

# Import the compiled UI module
from editorUi import Ui_Form

# The backend
import todo

# Misc.
from datetime import datetime

class editor(QtGui.QWidget):
    def __init__(self, parent, task=None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Start with no task item to edit
        self.item = None

    def edit(self, item):
        """Takes an item, loads the widget with the item's
        task contents, shows the widget"""
        self.item = None
        self.ui.task.setText(item.text)
        self.ui.done.setChecked(item.done)
        dt = item.date
        if dt:
            self.ui.dateTime.setDate(QtCore.QDate(dt.year, dt.month, dt.day))
            self.ui.dateTime.setTime(QtCore.QTime(dt.hour, dt.minute))
        else:
            self.ui.dateTime.setDateTime(QtCore.QDateTime())

        self.ui.tags.setText(','.join(t.name for t in item.tags))
        self.item = item
        self.show()

    def save(self):
        if self.item == None: return

        # Save date and time in the task
        d = self.ui.dateTime.date()
        t = self.ui.dateTime.time()

        self.item.date = datetime(
            d.year(),
            d.month(),
            d.day(),
            t.hour(),
            t.minute()
        )

        # Save text in the task
        self.item.text = unicode(self.ui.task.text())

        # Save tags.
        tags = [s.strip() for s in unicode(self.ui.tags.text()).split(',')]
        # For each tag, see if it is in the DB. If it is not, create it. If you had
        # a million tags, this would be very very wrong code
        self.item.tags = []
        for tag in tags:
            dbTag = todo.Tag.get_by(name=tag)
            if dbTag is None: # Tag is new, create it
                print "Creating tag: ", tag
                self.item.tags.append(todo.Tag(name=tag))
            else:
                self.item.tags.append(dbTag)

        # Display the data in the item
        #self.item.setText(0, self.item.text)
#        self.item.setText(1, str(self.item.date))
 #       self.item.setText(2, u','.join(t.name for t in self.item.tags))

        todo.saveData()
