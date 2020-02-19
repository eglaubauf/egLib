#####################################
#              LICENSE              #
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
        self.count = 0
        self.cams = self.get_cams()
        self.rop = self.setup_rop()
        self.create_takes()
        self.display_message()

    def get_cams(self):
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
        """Iterates over all selected Nodes and creates Takes"""
        if not self.cams:  # Return if there are no Cam Nodes
            return

        master_take = hou.takes.currentTake()

        for c in self.cams:
            # Check against OBJ-Level Nodes and Subnets
            child = master_take.addChildTake('take_' + c.name())
            hou.takes.setCurrentTake(child)
            child.addParmTuple(self.rop.parm("RS_renderCamera").tuple())
            self.rop.parm("RS_renderCamera").set(c.path())
            self.count += 1
        hou.takes.setCurrentTake(master_take)

    def display_message(self):
        """Displays the Count of Created Materials to the User"""
        if self.count > 0:
            hou.ui.displayMessage(str(self.count) + ' Takes have been created')
        else:
            hou.ui.displayMessage('Please select Camera-Nodes to create Takes')
