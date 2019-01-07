# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createdbdlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CreateDBDialog(object):
    def setupUi(self, CreateDBDialog):
        CreateDBDialog.setObjectName("CreateDBDialog")
        CreateDBDialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(CreateDBDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(CreateDBDialog)
        self.label.setGeometry(QtCore.QRect(0, 30, 81, 18))
        self.label.setObjectName("label")
        self.lineEditincfiles = QtWidgets.QLineEdit(CreateDBDialog)
        self.lineEditincfiles.setGeometry(QtCore.QRect(80, 30, 321, 21))
        self.lineEditincfiles.setObjectName("lineEditincfiles")
        self.label_2 = QtWidgets.QLabel(CreateDBDialog)
        self.label_2.setGeometry(QtCore.QRect(0, 10, 58, 18))
        self.label_2.setObjectName("label_2")
        self.lineEditrootdir = QtWidgets.QLineEdit(CreateDBDialog)
        self.lineEditrootdir.setGeometry(QtCore.QRect(80, 1, 311, 21))
        self.lineEditrootdir.setObjectName("lineEditrootdir")
        self.checkBox = QtWidgets.QCheckBox(CreateDBDialog)
        self.checkBox.setGeometry(QtCore.QRect(0, 60, 151, 23))
        self.checkBox.setObjectName("checkBox")
        self.label_3 = QtWidgets.QLabel(CreateDBDialog)
        self.label_3.setGeometry(QtCore.QRect(0, 90, 81, 18))
        self.label_3.setObjectName("label_3")
        self.lineEditexcldirs = QtWidgets.QLineEdit(CreateDBDialog)
        self.lineEditexcldirs.setGeometry(QtCore.QRect(80, 80, 311, 32))
        self.lineEditexcldirs.setObjectName("lineEditexcldirs")

        self.retranslateUi(CreateDBDialog)
        self.buttonBox.accepted.connect(CreateDBDialog.accept)
        self.buttonBox.rejected.connect(CreateDBDialog.reject)
        self.lineEditrootdir.editingFinished.connect(CreateDBDialog.update)
        QtCore.QMetaObject.connectSlotsByName(CreateDBDialog)

    def retranslateUi(self, CreateDBDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateDBDialog.setWindowTitle(_translate("CreateDBDialog", "Create disk database"))
        self.label.setText(_translate("CreateDBDialog", "include files"))
        self.label_2.setText(_translate("CreateDBDialog", "root dir"))
        self.checkBox.setText(_translate("CreateDBDialog", "Delete database"))
        self.label_3.setText(_translate("CreateDBDialog", "exclude dirs"))

