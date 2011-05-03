from PyQt4.QtCore import QAbstractItemModel, QModelIndex, Qt
from elixir import *
from todo import Task

class TodoTreeModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(TodoTreeModel, self).__init__(parent)

    def columnCount(self, parent=QModelIndex()):
        return 4


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
                    2: lambda task: ','.join([t.name for t in task.tags]),
                    3: lambda task: task.done
            }
            task = Task.query.all()[index.row()]
            return columnValues[index.column()](task)



    def flags(self, index):
        return super(TodoTreeModel, self).flags(index)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if (orientation == Qt.Horizontal
            and role == Qt.DisplayRole
            and 0 <= section < self.columnCount()):
            return {0:"Task", 1:"Date", 2:"Tags", 3:""}[section]

        return None

    def rowCount(self, parent=QModelIndex()):
        Task.query.count()

    def setData(self, index, value, role=Qt.EditRole):
        pass


