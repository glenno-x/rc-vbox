# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connection_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConnectionDialog(object):
    def setupUi(self, ConnectionDialog):
        ConnectionDialog.setObjectName("ConnectionDialog")
        ConnectionDialog.resize(390, 247)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ConnectionDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_user = QtWidgets.QLabel(ConnectionDialog)
        self.label_user.setObjectName("label_user")
        self.gridLayout.addWidget(self.label_user, 0, 0, 1, 1)
        self.lineEdit_user = QtWidgets.QLineEdit(ConnectionDialog)
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.gridLayout.addWidget(self.lineEdit_user, 0, 1, 1, 1)
        self.label_machine = QtWidgets.QLabel(ConnectionDialog)
        self.label_machine.setObjectName("label_machine")
        self.gridLayout.addWidget(self.label_machine, 1, 0, 1, 1)
        self.lineEdit_machine = QtWidgets.QLineEdit(ConnectionDialog)
        self.lineEdit_machine.setObjectName("lineEdit_machine")
        self.gridLayout.addWidget(self.lineEdit_machine, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConnectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(ConnectionDialog)
        self.buttonBox.accepted.connect(ConnectionDialog.accept)
        self.buttonBox.rejected.connect(ConnectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConnectionDialog)
        ConnectionDialog.setTabOrder(self.lineEdit_user, self.lineEdit_machine)

    def retranslateUi(self, ConnectionDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionDialog.setWindowTitle(_translate("ConnectionDialog", "Dialog"))
        self.label_user.setText(_translate("ConnectionDialog", "User"))
        self.label_machine.setText(_translate("ConnectionDialog", "Machine"))
