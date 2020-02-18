#####################################
#LICENSE                            #
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
"""
This script will create a Redshift Node Network based on a file selection

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import hou
import eg_createRSMat

class ApplyRSMat():
    """Applies an RS MAT to a Selection"""
    def __init__(self):
        self.context = hou.node("/mat")
        self.nodes = self.get_nodes()
        self.count = 0
        self.create_materials()
        self.display_message()
        

    def get_nodes(self):
        """Calls the Selected Nodes"""
        return hou.selectedNodes()

    def create_materials(self):
        """Iterates over all selected Nodes and applies a Material with Naming for each"""
        for n in self.nodes:
            #Check against OBJ-Level Nodes and Subnets
            if n.type().category() != hou.objNodeTypeCategory(): 
                break
            if not n.isSubNetwork():
                m = eg_createRSMat.RSMat(self.context, n.name())
                n.parm("shop_materialpath").set(m.get_path())
                self.count += 1

    def display_message(self):
        """Displays the Count of Created Materials to the User"""
        if self.count > 0:
            hou.ui.displayMessage(str(self.count) +' Materialnodes have been created')
        else:
            hou.ui.displayMessage('Please select OBJ-Nodes to create Materials')
