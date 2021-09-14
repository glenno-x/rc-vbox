from PyQt5.QtCore import (
    Qt, QAbstractListModel, QAbstractTableModel
)


class SettingsModel(QAbstractListModel):
    def __init__(self, *args, settings=None, **kwargs):
        super(SettingsModel, self).__init__(*args, **kwargs)
        self.settings = settings or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            label, text = self.settings[index.row()]
            return label + ' : ' + text
        '''
        if role == Qt.DecorationRole:
            label, _ = self.settings[index.row()]
            return label
        '''

    def rowCount(self, index):
        return len(self.settings)

