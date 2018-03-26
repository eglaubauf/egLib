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
import os
import shutil

########CONFIG ME HERE ###########
project = "Obscure"
tex = "tex"
light = "light"
############END CONFIG ############


site = hou.getenv("HSITE") + "/" + project + "/"
hipname = hou.getenv("HIPNAME")
hip = site + hipname
hiptex = hip + "/" + tex
hiplight = hip + "/" + light

errors = []

count = 0


def run():

    global count 
    

    mat = hou.node("/mat")
    nodes = mat.children()
    name = "materials"
    changeMats(nodes, name)
    text = str(count) + " Material-Textures successfully copied & changed"
    if count != 0:
        hou.ui.displayMessage(text)

    count = 0

    #Check Lights
    obj = hou.node("/obj")
    changeLights(obj.children())
    text = str(count) + " Light-Textures successfully copied & changed"
    if count != 0:
     hou.ui.displayMessage(text)

    if errors: 
        printErrors()


def changeMats(nodes, name):
    for n in nodes:
        if n.type().name() == "texture::2.0" or n.type().name() == "principledshader::2.0" or n.type().name() == "displacetexture" :
            for p in n.parms():
                if p.parmTemplate().type() == hou.parmTemplateType.String:
                    # Get Parm as String
                    s = p.evalAsString()
                    occur = s.rfind("/")
                    #Filter out non Files - go to next if none
                    if occur == -1:
                        continue
                    if s.startswith(hou.getenv("HSITE")):   #Leave if already in place
                        continue

                    filename = s[occur+1:]
                    path = s[:occur+1]

                    #Create Directories
                    matDir = hiptex+"/"+ name

                    if os.path.isdir(hip) is False:
                        os.makedirs(hip)
                        os.makedirs(hiptex)
                    elif os.path.isdir(hiptex) is False:
                        os.makedirs(hiptex)
                    if os.path.isdir(matDir) is False:
                        os.makedirs(matDir)

                    #Copy File to HSITE    
                    try:
                        shutil.copy(s,matDir)
                    except IOError, arg:
                       ex = s + ": "+ arg[1]
                       errors.append(ex)
                       continue

                    newPath = "$HSITE/" + project + "/" + hipname + "/" + tex + "/" + n.name() + "/" + filename
                    #print newPath
                    n.parm(p.name()).set(newPath)
                    global count
                    count += 1

        if n.type().name() == "materialbuilder":
            children = n.children() 
            name = n.name()    
            changeMats(children, name)
            name = "materials"


def changeLights(nodes):
   for n in nodes:
        if n.type().name() == "hlight::2.0" or n.type().name() == "envlight" or n.type().name() == "indirectlight" :
            for p in n.parms():
                if p.parmTemplate().type() == hou.parmTemplateType.String:    
                    if p.parmTemplate().type() == hou.parmTemplateType.String:
                        # Get Parm as String
                        s = p.evalAsString()
                        occur = s.rfind("/")
                        #Filter out non Files - go to next if none
                        if occur == -1:
                            continue
                        if s.startswith(hou.getenv("HSITE")):   #Leave if already in place
                            continue
                        if not os.path.exists(s):
                            continue 

                        filename = s[occur+1:]
                        path = s[:occur+1]

                        #Create Directories
                        matDir = hiplight+"/"

                        if os.path.isdir(hip) is False:
                            os.makedirs(hip)
                            os.makedirs(hiplight)
                        elif os.path.isdir(hiplight) is False:
                            os.makedirs(hiplight)
                        if os.path.isdir(matDir) is False:
                            os.makedirs(matDir)
                        
                        #Copy File to HSITE 
                        shutil.copy(s,matDir)

                        newPath = "$HSITE/" + project + "/" + hipname + "/" + light + "/" + n.name() + "/" + filename
                        #print newPath
                        n.parm(p.name()).set(newPath)
                        global count
                        count += 1


def printErrors():

    msg = "I failed to copy this Files: \n\n"
    for s in errors:
        msg = msg + s
        msg = msg + "\n"

    hou.ui.displayMessage(msg)
