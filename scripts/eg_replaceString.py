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
This script will check all Parms in all Nodes for a String and replaces it

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""

import hou
import re


message = "Search for Text in Strings"
labels = ["Search for","Replace Wih"]
def run():
    

    num, msg = hou.ui.readMultiInput(message, labels, buttons=('Ok', 'Cancel'))
    if num == 1:
        return
    
    #Check Geo 
    nodes = hou.node("/obj").children()
    objText = str(changeNodes(nodes,msg[0], msg[1], 0)) + " Parms in OBJ successfully changed"

    #Check Mat
    nodes = hou.node("/mat").children()
    matText = str(changeNodes(nodes, msg[0], msg[1], 0)) + " Parms in MAT successfully changed"

    #Check Cops
    nodes = hou.node("/img").children()
    imgText = str(changeNodes(nodes, msg[0], msg[1], 0)) + " Parms in COPs successfully changed"

    #Check Rop
    nodes = hou.node("/out").children()
    ropText = str(changeNodes(nodes, msg[0], msg[1], 0)) + " Parms in ROPs successfully changed"

    #Check Shop
    nodes = hou.node("/shop").children()
    shopText = str(changeNodes(nodes, msg[0], msg[1], 0)) + " Parms in SHOPs successfully changed"

   
    text = objText + "\n\n" +  matText + "\n\n" + imgText + "\n\n" + ropText + "\n\n" + shopText
    hou.ui.displayMessage(text)


def changeNodes(nodes, this, that, count):
    
    for n in nodes: 
        #Go For SOPs Dops and Everything
        if n.children() is not None:
            count = changeNodes(n.children() ,this, that, count)
        
        parms = n.parms()
        #Replace all Parms which are strings for the searched Value
        for p in parms:
            s =  p.evalAsString()
            if s.find(this) is not -1 :
                    newS = s.replace(this, that)
                    
                    n.parm(p.path()).set(newS)
                    count += 1
    return count     
