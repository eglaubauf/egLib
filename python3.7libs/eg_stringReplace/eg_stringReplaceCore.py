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


class Core():

    def __init__(self):
        self.rows = []
        self.hidden = 0
        self.ids = 0

    def clear_rows(self):
        '''Empties all Rows '''
        self.rows = []
        self.ids = 0

    def get_rows(self):
        '''Returns all visible Rows from Rows'''
        visible = []
        for row in self.rows:
            if row.get_display() is True:
                visible.append(row)
        return visible

    def load(self):
        '''Reads Parms from Houdini File '''
        self.clear_rows()
        for parm, path in hou.fileReferences():
            if parm:
                if parm.node().type().name() != "inline":
                    row = Row()
                    row.set_node(parm.node())
                    row.set_parm(parm)
                    # Check if string parm
                    print(parm.node())
                    print(parm.name())
                    if parm.parmTemplate().type() == hou.parmTemplateType.String:
                        try:
                            row.set_path(parm.unexpandedString())
                        except hou.OperationFailed:
                            row.set_path(parm.expression())
                        try:
                            row.set_new_path(parm.unexpandedString())
                        except hou.OperationFailed:
                            row.set_new_path(parm.expression())
                    else:
                        row.set_path(parm.evalAsString())
                        row.set_new_path(parm.evalAsString())
                    row.set_id(self.ids)
                    self.ids += 1
                    self.rows.append(row)

    def get_row(self, row_num):
        '''Returns a Single Row from Local Parms'''
        if self.rows[row_num]:
            row = [self.parms[row_num].evalAsString(), self.nodes[row_num], self.paths[row_num], self.new_paths[row_num]]
            return row
        return None

    def show(self, val):
        for row in self.rows:
            if row.get_data().get('node').startswith(val):
                row.set_display(True)
                self.hidden -= 1

    def hide(self, val):
        for row in self.rows:
            if row.get_data().get('node').startswith(val):
                row.set_display(False)
                self.hidden += 1


    def search(self, pattern, replace):
        for row in self.rows:
            path = row.get_data()['path']
            if path.find(pattern) > -1:
                new_path = path.replace(pattern, replace)
                row.set_new_path(new_path)

    def execute(self, selected_rows):

        for row in self.rows:
            if selected_rows:
                if row.get_id() in selected_rows:
                    if row.get_display() is True:
                        row.get_actual_parm().set(row.get_new_parm())
            else:
                if row.get_display() is True:
                    row.get_actual_parm().set(row.get_new_parm())


class Row:

    def __init__(self):
        self.display = True
        self.node = None
        self.parm = None
        #  Actual Table Data
        self.data = {
            'parm': '',
            'node': '',
            'path': '',
            'new_path': '',
            'id': -1
        }

    def set_display(self, flag):
        self.display = flag

    def get_display(self):
        return self.display

    def set_id(self, ids):
        self.data['id'] = ids

    def get_id(self):
        return self.data['id']

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def get_actual_parm(self):
        return self.parm

    def set_path(self, path):
        self.data['path'] = path

    def set_node(self, node):
        self.node = node
        self.data['node'] = node.path()

    def set_parm(self, parm):
        self.parm = parm
        self.data['parm'] = parm.parmTemplate().label()

    def set_new_path(self, new_path):
        self.data['new_path'] = new_path

    def get_new_parm(self):
        return self.data['new_path']
