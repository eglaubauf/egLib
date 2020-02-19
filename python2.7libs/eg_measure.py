#####################################
#     LICENSE                       #
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
This script creates a Distance Measure Node with two nulls for easy movement attached.
qLib is required.

Needs qLib Library installed:  https://github.com/qLab/qLib-dev

Feel free to comment/edit/contact me for further development.
Currently only tested on Windows

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""

import hou


def run():
    # Set Context
    obj = hou.node("/obj")

    start = None
    end = None
    nodes = hou.selectedNodes()
    move = False
    if len(nodes) == 0:
        move = True
        # Create Nodes
        start = obj.createNode("null")
        start.setName("start", True)
        start.parm("tx").set("2")

        end = obj.createNode("null")
        end.setName("end", True)
    elif len(nodes) == 1:

        start = nodes[0]
        end = obj.createNode("null")
        end.setName("end", True)
    else:
        start = nodes[0]
        end = nodes[1]

    # Create Dist Node
    dist = obj.createNode("qLib::distance_ql")
    # Connect
    dist.setInput(0, start)
    dist.setInput(1, end)

    # NetworkBox
    nBox = obj.createNetworkBox()
    nBox.addItem(start)
    nBox.addItem(end)
    nBox.addItem(dist)

    # Move
    if move is True:
        start.moveToGoodPosition()
    end.moveToGoodPosition()
    dist.moveToGoodPosition()
