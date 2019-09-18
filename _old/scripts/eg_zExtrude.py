#####################################
#LICENSE                            #
#####################################
#
# Copyright (C) 2019  Elmar Glaubauf
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
This script will extrude along a Normal?

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import hou
import soptoolutils

def run(kwargs):
 

    #Get Selected Node
    selNodes = hou.selectedNodes()

    #Create Node
    mrg = soptoolutils.genericTool(kwargs, 'polyextrude::2.0')


    #Set Parms
    curNode = kwargs["pane"].currentNode()
    curNode.parm('xformfront').set("1")
    curNode.parm('xformspace').set("global")

    #Set Display Flag
    mrg.setDisplayFlag(True)
    mrg.setRenderFlag(True)