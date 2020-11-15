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

import hou


def run():  # our cam object

    obj = hou.node("/obj")

    cam = createCam()
    setAutoFocus(cam)

    # Create Preview Frame
    prev = obj.createNode("null")
    prev.setName("AF_Preview", True)

    prev.setInput(0, cam, 0)

    prev.parm("controltype").set(3)
    prev.parm("orientation").set(3)
    prev.parm("dcolorr").set(0.9)
    prev.parm("dcolorg").set(0)

    parm_dict = {"tz": "-ch( opinputpath('.', 0)+'/focus')"}
    prev.setParmExpressions(parm_dict)

    # Create Dummy Target
    target = obj.createNode("null")
    target.setName("Target", True)
    target.parm("tz").set(-1)
    cam.parm("target").set(target.path())

    prev.moveToGoodPosition()
    target.moveToGoodPosition()


def createCam():

    # Set Context
    obj = hou.node("/obj")

    # Create Camera
    cam = obj.createNode("cam")
    cam.parm('resx').set('1920')
    cam.parm('resy').set('1080')
    cam.parm('near').set('0.01')

    cam_group = cam.parmTemplateGroup()
    cam_folder = hou.FolderParmTemplate("folder", "Autofocus")

    cam_folder.addParmTemplate(hou.FloatParmTemplate("distance", "Distance", 1))
    cam_folder.addParmTemplate(hou.StringParmTemplate("target", "Target", 1))

    cam_group.append(cam_folder)
    cam.setParmTemplateGroup(cam_group)

    return cam


def setAutoFocus(cam):

    afScript = """
    cam = hou.pwd()

    # get 4x4 matrix representing  transformation of our camera
    cam_xform = cam.worldTransform()

    # get position of our camera
    cam_pos = hou.Vector4(0, 0, 0, 1) * cam_xform
    cam_pos = hou.Vector3(cam_pos)

    # view axis of our camera
    view_axis = hou.Vector4(0, 0, -1, 0) * cam_xform

    # get target path
    target_path = cam.evalParm("target")
    # get target object
    target_node = hou.node(target_path)
    # get target's transformation
    target_xform = target_node.worldTransform()
    # get target's position
    target_pos = hou.Vector4(0, 0, 0, 1) * target_xform

    # cast from Vector4 to Vector3
    view_axis = hou.Vector3(view_axis)
    target_pos = hou.Vector3(target_pos)

    # normalize our view axis
    view_axis = view_axis.normalized()

    # get a vector pointing from camera to target
    cam_target = hou.Vector3( target_pos - cam_pos )

    # project cam_target vector on view_axis, because view_axis is normalized, this results in length of our projected vector, what represents focus distance in our case
    focus_dist = cam_target.dot(view_axis)

    return focus_dist"""

    parm_dict = {"distance": afScript}
    cam.setParmExpressions(parm_dict, language=hou.exprLanguage.Python)

    parm_dict = {"focus": "ch('distance')"}
    cam.setParmExpressions(parm_dict)
