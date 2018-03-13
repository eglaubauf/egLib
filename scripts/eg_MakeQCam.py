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
This script creates a Camera at the Origin, with qLib Frustum and qLib Rig attached.
The Nodes will be colored and Grouped into a NetworkBox.

Needs qLib Library installed:  https://github.com/qLab/qLib-dev

Feel free to comment/edit/contact me for further development.
Currently only tested on Windows

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""

import hou

def run():
    #Set Context
    obj = hou.node("/obj")

    ##########################
    # Cam
    ##########################
    myCam = obj.createNode("cam")
    myCam.parm('resx').set('1920')
    myCam.parm('resy').set('1080')
    myCam.parm('near').set('0.01')


    ##########################
    # Frustum
    ##########################
    frust = obj.createNode("qLib::camera_frustrum_ql")

    #Connect Camera
    frust.parm('camera').set(myCam.path())
    #Set Parms
    frust.parm('near').set('0.1')
    frust.parm('far').set('30')
    frust.parm('renderable').set('0')

    ##########################
    # Rig
    ##########################
    rig = obj.createNode('qLib::camera_rig_ql')
    #SetParent
    myCam.setInput(0,rig,0)

    ##########################
    #NetworkBox
    ##########################
    nBox = obj.createNetworkBox()
    #AddItems
    nBox.addItem(rig)
    nBox.addItem(myCam)
    nBox.addItem(frust)
    nBox.setComment('Camera')

    #LayoutNodes
    rig.moveToGoodPosition()
    myCam.moveToGoodPosition()
    frust.moveToGoodPosition()

    #Color
    rig.setColor(hou.Color((0,0.7,0.5)))
    myCam.setColor(hou.Color((0,0.7,0.5)))
    frust.setColor(hou.Color((0,0.7,0.5)))

    #SetPickingFlags
    myCam.parm('picking').set('0')
    frust.parm('picking').set('0')
