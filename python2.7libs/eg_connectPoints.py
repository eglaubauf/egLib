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

import toolutils
import hou


def run():

    # Get GeometrySelection
    geoSelection = toolutils.sceneViewer().selectGeometry()

    # Selection
    selectionStrings = geoSelection.selectionStrings()

    # NETWORKPANE STUFF
    # Get Selected Node in Network Pane
    selNode = hou.selectedNodes()

    # Create Split Node
    split = selNode[0].parent().createNode("polycut")
    # Connect
    split.setInput(0, selNode[0], 0)

    # WRONG FORMAT
    split.parm('cutpoints').set(selectionStrings[0])
    split.parm('strategy').set("cut")

    # Arrange Stuff
    split.moveToGoodPosition()
    split.setDisplayFlag(True)
    split.setSelected(1, 1, 0)
