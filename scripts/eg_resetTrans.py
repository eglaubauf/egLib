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
This script resets the selected Obj-Nodes Transforms to Zero.
Transformation Mode (Translate, Rotate, Scale, Pivot) is choosable.

Feel free to comment/edit/contact me for further development.
Currently only tested on Windows

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""


import soptoolutils
import objecttoolutils
import hou

def run():
    #helper
    translate = rotate = scale = uniform = pivot = 0

    #Get Selected Nodes
    selNodes = hou.selectedNodes()
    #Possible Choices
    choices = ["Translate", "Rotate", "Scale", "Uniform Scale", "Pivot" ]
    defaultChoices = [0,1,2,3,4]
    #Create Dialog
    selected = hou.ui.selectFromList( choices , default_choices = defaultChoices, message="Reset Transforms", num_visible_rows=1)

    #Get Data out of Tuple
    for elem in selected:
        if elem == 0:
            translate = 1
        if elem == 1:
            rotate = 1
        if elem == 2:
            scale = 1
        if elem == 3:
            uniform = 1
        if elem == 4:
            pivot = 1


    #For each selected Node Reset Transforms
    for x, node in enumerate(selNodes):
        #Translate
        if translate == 1:
            node.parm('tx').set("0")
            node.parm('ty').set("0")
            node.parm('tz').set("0")
        #Rotate
        if rotate == 1:
            node.parm('rx').set("0")
            node.parm('ry').set("0")
            node.parm('rz').set("0")
        #Scale
        if scale == 1:
            node.parm('sx').set("1")
            node.parm('sy').set("1")
            node.parm('sz').set("1")
        #Uniform Scale
        if uniform == 1:
            node.parm('scale').set("1")
        #Pivot
        if pivot == 1:
            node.parm('px').set("0")
            node.parm('py').set("0")
            node.parm('pz').set("0")
