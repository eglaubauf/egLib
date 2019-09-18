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
This script will align two Nodes at Object Level.
It needs two nodes selected. The Second gets transformed to the first one.
Transformation Mode (Translate, Rotate, Scale, Pivot) is choosable.

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import soptoolutils
import objecttoolutils
import hou

def run():
    #helper var
    translate = rotate = scale = uniform = pivot = 0

    #Get Selected Nodes
    selNodes = hou.selectedNodes()

    if len(selNodes) < 2:
        msg = ["Okay"]
        hou.ui.displayMessage("Please Select exactly 2 Nodes", msg, severity=hou.severityType.Message)
        return
    else:
        #Possible Choices
        choices = ["Translate", "Rotate", "Scale", "Pivot" ]
        defaultChoices = [0,1,2]
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
                pivot = 1
    
   

    #For each selected Node Reset Transforms
    for index in range(len(selNodes)):
        #Translate
        if translate == 1:
            selNodes[index].parm('tx').set(selNodes[0].parm('tx').evalAsString())
            selNodes[index].parm('ty').set(selNodes[0].parm('ty').evalAsString())
            selNodes[index].parm('tz').set(selNodes[0].parm('tz').evalAsString())
        #Rotate
        if rotate == 1:
            selNodes[index].parm('rx').set(selNodes[0].parm('rx').evalAsString())
            selNodes[index].parm('ry').set(selNodes[0].parm('ry').evalAsString())
            selNodes[index].parm('rz').set(selNodes[0].parm('rz').evalAsString())
        #Scale
        if scale == 1:
            selNodes[index].parm('sx').set(selNodes[0].parm('sx').evalAsString())
            selNodes[index].parm('sy').set(selNodes[0].parm('sy').evalAsString())
            selNodes[index].parm('sz').set(selNodes[0].parm('sz').evalAsString())
        #Pivot
        if pivot == 1:
            selNodes[index].parm('px').set(selNodes[0].parm('px').evalAsString())
            selNodes[index].parm('py').set(selNodes[0].parm('py').evalAsString())
            selNodes[index].parm('pz').set(selNodes[0].parm('pz').evalAsString())
