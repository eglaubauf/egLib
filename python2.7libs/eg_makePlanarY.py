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
This evens out the selected Vertices in Y-Direction - Makes them planar along World Y

Feel free to comment/edit/contact me for further development.
Currently only tested on Windows

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""

import toolutils


def run():
    # Get Points in Viewport
    gs = toolutils.sceneViewer().selectGeometry()
    sS = gs.selectionStrings()
    s = gs.selections()
    if gs:
        if gs.nodes():
            n = gs.nodes()[0]
            geo = n.geometry()
            points = s[0].points(geo)
            selNode = n

            # NETWORKPANE STUFF
            # Get Selected Node in Network Pane
            # selNode = hou.selectedNodes()

            if selNode:
                # Create Wrangle Node
                edit = selNode.parent().createNode("edit")
                # Connect
                edit.setInput(0, selNode, 0)
                # Set Group
                edit.parm("group").set(sS[0])

                #############################
                # Calc Pos
                #############################
                pivX = 0
                pivY = 0
                pivZ = 0
                count = 0
                # Get Average PosX
                for point in points:
                    pos = point.position()
                    pivX += pos.x()
                    pivY += pos.y()
                    pivZ += pos.z()
                    count += 1
                # Calc
                pivX = pivX / count
                pivY = pivY / count
                pivZ = pivZ / count
                
                # CalcRotation of Parent
                rotX = -selNode.parent().parm("rx").eval()
                rotY = -selNode.parent().parm("ry").eval()
                rotZ = -selNode.parent().parm("rz").eval()
                # Counter Rotation of Parent 
                edit.parm("rx").set(rotX)
                edit.parm("ry").set(rotY)
                edit.parm("rz").set(rotZ)
                
                # SetParms
                edit.parm("px").set(pivX)
                edit.parm("py").set(pivY)
                edit.parm("pz").set(pivZ)

                # Set Pos
                edit.parm("sy").set("0")

                # Arrange Stuff
                edit.moveToGoodPosition()
                edit.setDisplayFlag(True)
                edit.setSelected(1, 1, 0)
                edit.setName("MakePlanarY", True)
