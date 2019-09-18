#####################################
#LICENSE                            #
#####################################
#
# Copyright (C) 2017  Elmar Glaubauf
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
This script will merge two or more Nodes at Sop Level.
If connected to a shortcut (like 'M') it will have Nuke like functionality.

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import soptoolutils
import hou

def run(kwargs):
    selNodes = hou.selectedNodes()
    valid = True

    for node in selNodes:
        type = node.type()
        if not hou.NodeType.category(type) == hou.sopNodeTypeCategory():
            valid = False
    if valid:
        mrg = soptoolutils.genericTool(kwargs, 'merge')
        
        for x, node in enumerate(selNodes):
            mrg.setNextInput(node)
        
        mrg.setDisplayFlag(True)
        mrg.setRenderFlag(True)
    else:
        hou.ui.displayMessage("Please select SOP-Level Nodes")
