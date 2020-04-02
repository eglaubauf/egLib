# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_StringReplacer(object):
    def setupUi(self, StringReplacer):
        StringReplacer.setObjectName("StringReplacer")
        StringReplacer.resize(870, 463)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StringReplacer.sizePolicy().hasHeightForWidth())
        StringReplacer.setSizePolicy(sizePolicy)
        StringReplacer.setMouseTracking(True)
        self.gridLayout = QtWidgets.QGridLayout(StringReplacer)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(StringReplacer)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lbl_searchLabel = QtWidgets.QLabel(StringReplacer)
        self.lbl_searchLabel.setObjectName("lbl_searchLabel")
        self.verticalLayout.addWidget(self.lbl_searchLabel)
        self.tbx_searchBox = QtWidgets.QLineEdit(StringReplacer)
        self.tbx_searchBox.setText("")
        self.tbx_searchBox.setObjectName("tbx_searchBox")
        self.verticalLayout.addWidget(self.tbx_searchBox)
        self.lbl_replaceLabel = QtWidgets.QLabel(StringReplacer)
        self.lbl_replaceLabel.setObjectName("lbl_replaceLabel")
        self.verticalLayout.addWidget(self.lbl_replaceLabel)
        self.tbx_replaceBox = QtWidgets.QLineEdit(StringReplacer)
        self.tbx_replaceBox.setObjectName("tbx_replaceBox")
        self.verticalLayout.addWidget(self.tbx_replaceBox)
        self.label = QtWidgets.QLabel(StringReplacer)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.cbx_rop = QtWidgets.QCheckBox(StringReplacer)
        self.cbx_rop.setChecked(True)
        self.cbx_rop.setObjectName("cbx_rop")
        self.verticalLayout.addWidget(self.cbx_rop)
        self.cbx_obj = QtWidgets.QCheckBox(StringReplacer)
        self.cbx_obj.setChecked(True)
        self.cbx_obj.setObjectName("cbx_obj")
        self.verticalLayout.addWidget(self.cbx_obj)
        self.cbx_mat = QtWidgets.QCheckBox(StringReplacer)
        self.cbx_mat.setChecked(True)
        self.cbx_mat.setObjectName("cbx_mat")
        self.verticalLayout.addWidget(self.cbx_mat)
        self.cbx_cop = QtWidgets.QCheckBox(StringReplacer)
        self.cbx_cop.setChecked(True)
        self.cbx_cop.setObjectName("cbx_cop")
        self.verticalLayout.addWidget(self.cbx_cop)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.tableWidget = QtWidgets.QTableWidget(StringReplacer)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.bb_buttonBox = QtWidgets.QDialogButtonBox(StringReplacer)
        self.bb_buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.bb_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb_buttonBox.setObjectName("bb_buttonBox")
        self.verticalLayout.addWidget(self.bb_buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(StringReplacer)
        QtCore.QMetaObject.connectSlotsByName(StringReplacer)

    def retranslateUi(self, StringReplacer):
        _translate = QtCore.QCoreApplication.translate
        StringReplacer.setWindowTitle(_translate("StringReplacer", "RS Material Builder"))
        self.label_2.setText(_translate("StringReplacer", "Path Replace"))
        self.lbl_searchLabel.setText(_translate("StringReplacer", "Search"))
        self.lbl_replaceLabel.setText(_translate("StringReplacer", "Replace"))
        self.label.setText(_translate("StringReplacer", "Node Filter"))
        self.cbx_rop.setText(_translate("StringReplacer", "ROP Context"))
        self.cbx_obj.setText(_translate("StringReplacer", "OBJ Context"))
        self.cbx_mat.setText(_translate("StringReplacer", "MAT Context"))
        self.cbx_cop.setText(_translate("StringReplacer", "COP Context"))
