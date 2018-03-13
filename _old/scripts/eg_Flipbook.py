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
This script creates a Flipbook into $HIP/flipbook/camname. Camera Resolution is used.
If Cam is within a shotql node the name of shotql is used.

Feel free to comment/edit/contact me for further development.
Currently only tested on Windows

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import toolutils
import os
sc = toolutils.sceneViewer()

#Get Current View
view = sc.curViewport()

#Settings
s = sc.flipbookSettings()

#Set FrameRange
range = (hou.playbar.playbackRange())
s.frameRange(range)

#Set Resolution
cam = view.camera()
if cam != None: 
    res = (cam.evalParm('resx'),cam.evalParm('resy'))
    s.resolution(res)
    s.cropOutMaskOverlay(True)

    #Set Output Name and Path
    node = cam.parent().parent()
    if node.type().name() != "qLib::shot_ql::1":
        path = cam.name()
    else:
        path = cam.parent().parent().name()
        
    dir = hou.getenv('HIP')+'/'+'flipbook/' + path
    
    if not os.path.isdir(dir):
            os.makedirs(dir)
    path = '$HIP/flipbook/' + path + '/' + path + '_$F4.jpg'
    
    s.output(path)

    sc.flipbook(viewport = view, settings=s, open_dialog = False)
else:
    hou.ui.displayMessage('Please create a Camera')
print "-----------------------------------------"