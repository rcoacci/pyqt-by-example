from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt
from elixir import *
from todo import Task

class TodoTreeModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super(TodoTreeModel, self).__init__(parent)

    def columnCount(self, parent=QModelIndex()):
        return 3


    def data (self, index, role=Qt.DisplayRole):

        if not index.isValid():
            return None

        if not 0 <= index.row() < self.rowCount():
            return None

        if not 0 <= index.column() < self.columnCount():
            return None

        if role == Qt.DisplayRole:
            columnValues = {
                    0: lambda task: task.text,
                    1: lambda task: str(task.date),
                    2: lambda task: ','.join([tag.name for tag in task.tags]),
            }
            task = Task.query.all()[index.row()]
            return columnValues[index.column()](task)

        if role == Qt.CheckStateRole and index.column() == 0:
            task = Task.query.all()[index.row()]
            return Qt.Checked if task.done else Qt.Unchecked



    def flags(self, index):
        return super(TodoTreeModel, self).flags(index)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if (orientation == Qt.Horizontal
            and role == Qt.DisplayRole
            and 0 <= section < self.columnCount()):
            return {0:"Task", 1:"Date", 2:"Tags", }[section]

        return None

    def rowCount(self, parent=QModelIndex()):
        return int(Task.query.count())

    def setData(self, index, value, role=Qt.EditRole):
        pass

    def task(self, index):
        if not index.isValid():
            return None

        if not 0 <= index.row() < self.rowCount():
            return None

        return Task.query.all()[index.row()]


