# -*- coding: utf-8 -*-

"""The user interface for our app"""

from PyQt4 import QtCore, QtGui
from todo_model import TodoTreeModel
from windowUi import Ui_MainWindow
import os
import sys
import todo

# Import Qt modules

# Import the compiled UI module

# Import our backend

# Create a class for our main window
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setStyleSheet("QHeaderView::section{border-style:none;}")

        # This is always the same
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Start with the editor hidden
        self.ui.editor.hide()

        # Let's do something interesting: load the database contents
        # into our task list widget
#        for task in todo.Task.query.all():
#            tags = ','.join([t.name for t in task.tags])
#            item = QtGui.QTreeWidgetItem([task.text, str(task.date), tags])
#            item.task = task
#            if task.done:
#                item.setCheckState(0, QtCore.Qt.Checked)
#            else:
#                item.setCheckState(0, QtCore.Qt.Unchecked)
#            self.ui.list.addTopLevelItem(item)
        self.ui.list.setModel(TodoTreeModel(self))
        self.ui.list.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.ui.list.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.ui.list.selectionModel().selectionChanged.connect(self.on_list_currentItemChanged)
        self.ui.list.currentItem = None


    def on_list_itemChanged(self, item, column):
        if item.checkState(0):
            item.task.done = True
        else:
            item.task.done = False
        todo.saveData()

    def on_actionDelete_Task_triggered(self, checked=None):
        if checked is None: return
        # First see what task is "current".
        item = self.ui.list.currentItem()

        if not item: # None selected, so we don't know what to delete!
            return
        # Actually delete the task
        item.task.delete()
        todo.saveData()

        # And remove the item. I think that's not pretty. Is it the only way?
        self.ui.list.takeTopLevelItem(self.ui.list.indexOfTopLevelItem(item))

    def on_list_currentItemChanged(self, current=None, previous=None):

        anySelected = bool(current and current.indexes()[0])
        # In Session 5, fixes a bug where an item was current but had no visible
        # changes, so it could be deleted/edited surprisingly.
#        if current:
#            current.setSelected(True)

        if anySelected:
            self.ui.list.currentItem = self.ui.list.model().task(current.indexes()[0])
        else:
            self.ui.list.currentItem = None

        # Changed in session 5, because we have more than one action
        # that should only be enabled only if a task is selected
        for action in  [self.ui.actionDelete_Task,
                        self.ui.actionEdit_Task,
                       ]:
            action.setEnabled(anySelected)
        if self.ui.editor.isVisible():
            self.on_actionEdit_Task_triggered(True)

    def on_actionNew_Task_triggered(self, checked=None):
        if checked is None: return
        # Create a dummy task
        task = todo.Task(text="New Task")

        # Create an item reflecting the task
        item = QtGui.QTreeWidgetItem([task.text, str(task.date), ""])
        item.setCheckState(0, QtCore.Qt.Unchecked)
        item.task = task

        # Put the item in the task list
        self.ui.list.addTopLevelItem(item)
        self.ui.list.setCurrentItem(item)
        # Save it in the DB
        todo.saveData()
        # Open it with the editor
        self.ui.editor.edit(item)

    def on_actionEdit_Task_triggered(self, checked=None):
        if checked is None: return

        # First see what task is "current".
        item = self.ui.list.currentItem

        if not item: # None selected, so we don't know what to edit!
            return

        # Open it with the editor
        self.ui.editor.edit(item)

def main():
    # Init the database before doing anything else
    todo.initDB()

    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

