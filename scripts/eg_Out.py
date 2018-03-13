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
This script creates a black Null Node and prompts for a name

Twitter: @eglaubauf 
Web: www.elmar-glaubauf.at
"""

import objecttoolutils
import soptoolutils
import re
import hou


def run(kwargs):

    #Get Selected Node
    selNodes = hou.selectedNodes()

    #mrg = selNodes[0].parent().createNode("null")
    #Create NULL
    kwargs['bbox'] = hou.BoundingBox(-0.5, -0.5, -0.5, 0.5, 0.5, 0.5)
    mrg = objecttoolutils.genericTool(kwargs, 'null')

    curNode = kwargs["pane"].currentNode()

    #Make InputField
    name = hou.ui.readInput("Call me Names", title="Name")[1]

    #Remove Special Chars and replace them with "_"
    for k in name.split("\n"):
        name = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
    name = name.upper()
    name = name.replace(" ", "_")



    #Connect Node to Predecessor
    if not kwargs['shiftclick']:
        for x, node in enumerate(selNodes):
            mrg.setNextInput(node)

    #SetInterface
    curNode.setName(name, True)
    curNode.setColor(hou.Color((0,0,0)))

    curNode.setDisplayFlag(True)
    curNode.setRenderFlag(True)