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
This script will copy data to the HSITE Directory. 
Files will be sorted into Directories by materialbuilder name. TopLevel Textures will not be sorted. 
Works recursevly. 
Environmentmaps from lights will also be copied to the HSITE directory. 
Please specifiy Project/Directory names as wanted below.
TODO: implement sorting based on connected materials. 


Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""

import hou
import re



########CONFIG ME HERE ###########
project = "Obscure"
geo = "geo"
tex = "tex"
light = "light"
newName = "toFarm"
############END CONFIG ############



message = "Search for Text in Strings"
labels = ["Search for","Replace Wih"]
def run():
    

    num, msg = hou.ui.readMultiInput(message, labels, buttons=('Ok', 'Cancel'))
    if num == 1:
        return



    mat = hou.node("/mat")
    nodes = mat.children()
    matCount = changeMats(nodes, msg[0], msg[1], 0)
    matText = str(matCount) + " Material-Textures successfully copied & changed"

    #Check Lights
    obj = hou.node("/obj")
    lightCount = changeLights(obj.children(), msg[0], msg[1])
    lightText = str(lightCount) + " Light-Textures successfully copied & changed"

    #Check Geo
    objCount = changeGeo(obj.children(),msg[0], msg[1], 0)
    objText = str(objCount) + " Geo-Files successfully copied & changed"
   
    text = "Materials: \n" + matText + "\n\n" +  "Lights: \n" + lightText + "\n\n" +  "Geometry: \n" + objText + "\n\n"
    hou.ui.displayMessage(text)

def changeMats(nodes, this, that, count):
    for n in nodes:
        for p in n.parms():
            if p.parmTemplate().type() == hou.parmTemplateType.String:
                # Get Parm as String
                s = p.evalAsString()
              
                if s.find(this) is not -1 :
                    newS = s.replace(this, that)
                    p.set(newS)
                    count += 1

        if n.type().name() == "materialbuilder":
            children = n.children() 
            name = n.name()    
            count = changeMats(children, this, that, count)
            name = "materials"
    return count



def changeGeo(nodes, this, that, count):
    for n in nodes:
        if n.type().name() == "subnet":
            count = changeGeo(n.children(),this, that, count)
        elif n.type().name() == "geo":
            #Iterate over Nodes on SOP Level
            for sop in n.children():
                if sop.type().name() == "file" or sop.type().name() == "filecache":
                    # Get Parm as String
                    s = sop.parm("file").evalAsString()
                
                    if s.find(this) is not -1 :
                        newS = s.replace(this, that)
                        sop.parm("file").set(newS)
                        count += 1
    return count


def changeLights(nodes,  this, that):
    count = 0
    for n in nodes:
        if n.type().name() == "hlight::2.0" or n.type().name() == "envlight" or n.type().name() == "indirectlight" :
            for p in n.parms():
                if p.parmTemplate().type() == hou.parmTemplateType.String:    
                    if p.parmTemplate().type() == hou.parmTemplateType.String:
                        # Get Parm as String
                        s = p.evalAsString()
                        
                        if s.find(this) is not -1 :
                            newS = s.replace(this, that)
                            p.set(newS)
                            count += 1
    return count
