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
This script will import Geometry Files based on their name into separate Nodes. 
The Geometry is parsed for "Collide" and "Render". Renderfiles can optionially loaded in as Packed Disk Primitives. 
(Selection Dialog)

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""


import hou
import os
import re

obj = hou.node("/obj")

def run():
    files = hou.ui.selectFile(title="Please choose Files to import", collapse_sequences = False, multiple_select = True, file_type = hou.fileType.Geometry)
    if files is "":
        return
    
    r_as_pprim = hou.ui.displayMessage("RenderMesh as Packed Primitive?", buttons=("Yes", "No"))
            
    strings = files.split(";")
    
    for i, s in enumerate(strings):
        s = s.rstrip(' ')
        s = s.lstrip(' ')
        
        #Get Name of File
        name = s.split(".")
        k = name[0].rfind("/")
        name = name[0][k+1:]
    
        #Create File Node
        currNode = obj.createNode("geo", node_name = name )
        currNode.moveToGoodPosition()
        c = currNode.children()
        
        c[0].parm('file').set(s)
        c[0].setName(name, True)
        #TO DO - Insert Menu Option her
        if "Render" in name:
            if not r_as_pprim:
                c[0].parm('loadtype').set(4)
                c[0].parm('viewportlod').set(0)
        
        null = currNode.createNode("null")
        
        null.setNextInput(c[0])
        
        null.setName("OUT", True)
        null.setColor(hou.Color((0,0,0)))
        
        null.setDisplayFlag(True)
        null.setRenderFlag(True)
        
        null.moveToGoodPosition()
        