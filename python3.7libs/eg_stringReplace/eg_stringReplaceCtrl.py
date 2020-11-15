#####################################
#           LICENSE                 #
#####################################
#
# Copyright (C) 2020  Elmar Glaubauf
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import hou

from PySide2 import QtWidgets, QtCore

import eg_stringReplaceCore as core
import view as view

# Where is this script?
# SCRIPT_LOC = os.path.split(__file__)[0]

import importlib
importlib.reload(core)
importlib.reload(view)

'''
Open with

import eg_stringReplace.eg_stringReplaceCtrl as link
reload(link)
link.open()


'''

develop = False
tmpWindow = None


def open(develop=False):

    if develop:
        reload(core)
        reload(view)
    try:
        tmpWindow.close()
    except:
        pass

    tmpWindow = Controller()
    tmpWindow.show()


class Controller(QtWidgets.QDialog, view.Ui_StringReplacer):

    def __init__(self, parent=hou.qt.mainWindow()):
        super(Controller, self).__init__(parent)

        self.setupUi(self)

        # Set Houdini Style to Window
        self.setProperty("houdiniStyle", True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.core = core.Core()
        self.create_connections()

        #self.init_filters()
        self.core.load()
        self.init_table()
        self.update_table()

    # linking Buttons to Functions
    def create_connections(self):

        self.tbx_searchBox.textChanged.connect(self.search)
        self.tbx_replaceBox.textChanged.connect(self.search)

        self.cbx_mat.toggled.connect(self.filter_mat)
        self.cbx_obj.toggled.connect(self.filter_obj)
        self.cbx_rop.toggled.connect(self.filter_rop)
        self.cbx_cop.toggled.connect(self.filter_cop)

        self.bb_buttonBox.rejected.connect(self.destroy)
        self.bb_buttonBox.accepted.connect(self.execute)

    def search(self):
        self.core.search(self.tbx_searchBox.text(), self.tbx_replaceBox.text())
        self.update_table()

    def reset(self):
        self.core.loadParms()

    def init_filters(self):
        self.core.show('/obj')
        self.core.show('/mat')
        self.core.show('/shop')
        self.core.show('/out')
        self.core.show('/img')

    def init_table(self):
        '''Create the Table Header'''
        count = 5
        column_names = ['Node', 'Parm', 'Path', 'NewPath', 'id']

        self.tableWidget.setColumnCount(count)
        self.tableWidget.setHorizontalHeaderLabels(column_names)

    def get_dict_entry(self, row, num):
        if num == 0:
            return row.get_data()['node']
        elif num == 1:
            return row.get_data()['parm']
        if num == 2:
            return row.get_data()['path']
        if num == 3:
            return row.get_data()['new_path']
        if num == 4:
            return row.get_data()['id']

    def update_table(self):
        '''Draw a new Table'''
        # Build Table Content

        rows = self.core.get_rows()

        self.tableWidget.reset()

        self.tableWidget.setRowCount(len(rows))

        for row_num, row in enumerate(rows):
            column_num = 0
            while column_num < 5:
                cell = self.get_dict_entry(row, column_num)
                if row.get_display():
                    item = QtWidgets.QTableWidgetItem()
                    item.setData(0, cell)
                    self.tableWidget.setItem(row_num, column_num, item)
                column_num += 1
        self.tableWidget.setColumnHidden(4, True)
        self.tableWidget.resizeColumnsToContents()

    def filter_obj(self):
        if self.cbx_obj.isChecked():
            self.core.show('/obj')
        else:
            self.core.hide('/obj')
        self.update_table()

    def filter_mat(self):
        if self.cbx_mat.isChecked():
            self.core.show('/mat')
            self.core.show('/shop')
        else:
            self.core.hide('/mat')
            self.core.hide('/shop')
        self.update_table()

    def filter_rop(self):
        if self.cbx_rop.isChecked():
            self.core.show('/out')
        else:
            self.core.hide('/out')
        self.update_table()

    def filter_cop(self):
        if self.cbx_cop.isChecked():
            self.core.show('/img')
        else:
            self.core.hide('/img')
        self.update_table()

    def get_selection(self):
        self.tableWidget.setColumnHidden(4, False)
        items = self.tableWidget.selectedItems()

        selected_rows = []
        for num, i in enumerate(items, 0):
            if (num % 5) == 4:
                selected_rows.append(int(i.text()))
        return selected_rows

    # Execute Material Creation
    def execute(self):
        sel = self.get_selection()
        if sel:
            self.core.execute(sel)
            self.destroy()
            return
        if hou.ui.displayConfirmation('Nothing Selected. Do you want to replace all visible Rows?'):
            self.core.execute(sel)
            self.destroy()
        return
