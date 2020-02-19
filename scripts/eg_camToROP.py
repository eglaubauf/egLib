#####################################
# LICENSE                            #
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
Sets the Current camera for Rendering with Redshift

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import hou


def run():  # our cam object
    """Runs the Script"""

    pane_tab = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)

    if pane_tab:
        cam = pane_tab.curViewport().camera()
    if not cam:
        cam = create_cam()
        pane_tab.curViewport().saveViewToCamera(cam)
        pane_tab.curViewport().setCamera(cam)
        set_cam_for_render(cam)
    else:
        hou.ui.displayMessage("No Viewport found")
        # Check if this a PaneTab of Type SceneViewer


def set_cam_for_render(cam):
    """Sets the given Camera in the active Render ROP"""

    out = hou.node("/out")

    for o in out.children():
        if o.type().name() == "Redshift_ROP":
            o.parm("RS_renderCamera").set(cam.path())
            return

    rop = out.createNode("Redshift_ROP")
    rop.parm("RS_renderCamera").set(cam.path())

    return


def create_cam():

    # Set Context
    obj = hou.node("/obj")

    # Create Camera
    cam = obj.createNode("cam")

    cam.parm('resx').set('1920')
    cam.parm('resy').set('1080')
    cam.parm('near').set('0.01')

    return cam
