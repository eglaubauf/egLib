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


class TakesFromCams():
    """Creates Takes from the Selected Cams for the First RS-ROP found"""
    def __init__(self):
        self.nodes = self.get_nodes()
        self.count = 0
        self.rop = self.set_rop()
        self.create_takes()
        self.display_message()


    def get_nodes(self):
        """Calls the Selected Camera Nodes"""
        cams = []
        for c in hou.selectedNodes():
            if c.type().name() == "cam":
                cams.append(c)

        return cams

    def setup_rop(self):
        """Gets the current Redshift ROP"""

        out = hou.node("/out")

        for o in out.children():
            if o.type().name() == "Redshift_ROP":
                return o

        rop = out.createNode("Redshift_ROP")
        return rop


    def create_takes(self):
        """Iterates over all selected Nodes and applies a Material with Naming for each"""
        if not self.nodes: # Return if there are no Cam Nodes
            return

        master_take = hou.takes.currentTake()

        my = hou.takes.currentTake()
        for n in self.nodes:
            #Check against OBJ-Level Nodes and Subnets
                child = master_take.addChildTake(n.name()+"_take")
                child.
                child.addParmTuplesFromNode(self.rop)
                self.count += 1


    def display_message(self):
        """Displays the Count of Created Materials to the User"""
        if self.count > 0:
            hou.ui.displayMessage(str(self.count) +' Takes have been created')
        else:
            hou.ui.displayMessage('Please select Camera-Nodes to create Takes')
