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
This script creates a Trajectory for the selected Node

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""

import hou


def run():
    # Get Selected Node
    selNodes = hou.selectedNodes()

    if selNodes:
        if len(selNodes) < 2:
            obj = hou.node("/obj")
            geoNode = obj.createNode("geo")
            geoNode.setName("trajectory", True)
            geoNode.moveToGoodPosition()
            # geoNode.children()[0].destroy()

            trail = geoNode.createNode("qLib::motion_trail_ql")
            trail.parm('target').set(selNodes[0].path())
        else:
            hou.ui.displayMessage("Please Select just 1 Node", severity=hou.severityType.Message)
    else:
        hou.ui.displayMessage("Please Select a Node", severity=hou.severityType.Message)
