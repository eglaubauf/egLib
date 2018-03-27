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
geo = "geo"
tex = "tex"
light = "light"
############END CONFIG ############


site = hou.getenv("HSITE") + "/" + project + "/"
hipname = hou.getenv("HIPNAME")
hip = site + hipname
hiptex = hip + "/" + tex
hiplight = hip + "/" + light
hipGeo = hip + "/" + geo

errors = []

overwrite = 0

def run():
    
    global overwrite
    global errors
    overwrite = hou.ui.displayMessage(text = "Overwrite existing?", buttons=('No','Yes', 'Cancel'), close_choice=2)
    if overwrite == 2:
        return
    print overwrite

    mat = hou.node("/mat")
    nodes = mat.children()
    name = "materials"
    matCount = changeMats(nodes, name, 0)
    matText = str(matCount) + " Material-Textures successfully copied & changed"

    #Check Lights
    obj = hou.node("/obj")
    lightCount = changeLights(obj.children())
    lightText = str(lightCount) + " Light-Textures successfully copied & changed"

    #Check Geo
    objCount = changeGeo(obj.children(), 0)
    objText = str(objCount) + " Geo-Files successfully copied & changed"

    text = "Materials: \n" + matText + "\n\n" +  "Lights: \n" + lightText + "\n\n" +  "Geometry: \n" + objText + "\n\n" 
    
    if errors: 
        text = printErrors(text)
    hou.ui.displayMessage(text)

def changeGeo(nodes, count):
    for n in nodes:
        if n.type().name() == "subnet":
            count = changeGeo(n.children(), count)
        elif n.type().name() == "geo":
            #Iterate over Nodes on SOP Level
            for sop in n.children():
                if sop.type().name() == "file" or sop.type().name() == "filecache":
                    if sop.parm("filemode") != "write":
                        # Get Parm as String
                        s = sop.parm("file").evalAsString()
                        occur = s.rfind("/")
                        #Filter out non Files - go to next if none
                        if occur == -1:
                            continue
                        if s.startswith(hou.getenv("HSITE")):   #Leave if already in place
                            continue   
                        if not os.path.exists(s):
                            #global errors
                            s = (s + " does not exist")
                            errors.append(s)
                            continue 

                        filename = s[occur+1:]
                        path = s[:occur+1]

                        #Create Directories
                        geoDir = hipGeo + "/" + n.name()

                        if os.path.isdir(hip) is False:
                            os.makedirs(hip)
                            os.makedirs(hipGeo)
                        elif os.path.isdir(hipGeo) is False:
                            os.makedirs(hipGeo)
                        if os.path.isdir(geoDir) is False:
                            os.makedirs(geoDir)

                        #Copy File to HSITE   
                        global overwrite
                        if overwrite:      
                            if not s.startswith("op:/"):
                                if not copy(s, geoDir):
                                    continue
                        else:
                            if os.path.exists(hou.getenv("HSITE") + "/" + project + "/" + hipname + "/" + geo + "/" + n.name() + "/" + filename):
                                continue    
                            elif not copy(s, geoDir):
                                continue


                        newPath = "$HSITE/" + project + "/" + hipname + "/" + geo + "/" + n.name() + "/" + filename
                        #newPath to Parm
                        sop.parm("file").set(newPath)
                        sop.parm("loadtype").set("packedseq") #Workaround for PackedPrims on Network Drives
                        count += 1
    return count


def changeMats(nodes, name, count):
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
                    if not os.path.exists(s):
                        #global errors
                        s = (s + " does not exist")
                        errors.append(s)
                        continue

                    filename = s[occur+1:]
                    path = s[:occur+1]

                    #Create Directories
                    matDir = hiptex+"/" + name 

                    if os.path.isdir(hip) is False:
                        os.makedirs(hip)
                        os.makedirs(hiptex)
                    elif os.path.isdir(hiptex) is False:
                        os.makedirs(hiptex)
                    if os.path.isdir(matDir) is False:
                        os.makedirs(matDir)

                    #Copy File to HSITE   
                    global overwrite
                    if overwrite:
                        if not s.startswith("op:/"):      
                            if not copy(s, matDir):
                                continue
                    else:
                        if os.path.exists(hou.getenv("HSITE") + "/" + project + "/" + hipname + "/" + tex + "/" + name + "/" + filename):
                            continue    
                        elif not copy(s, matDir):
                            continue

                    newPath = "$HSITE/" + project + "/" + hipname + "/" + tex + "/" + name + "/" + filename
                    #newPath to Parm
                    n.parm(p.name()).set(newPath)
                    count += 1

        if n.type().name() == "materialbuilder":
            children = n.children() 
            name = n.name()    
            count = changeMats(children, name, count)
            name = "materials"
    return count


def changeLights(nodes):
    count = 0
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

                        filename = s[occur+1:]
                        path = s[:occur+1]

                        #Create Directories
                        lightDir = hiplight+ "/" + n.name()

                        if os.path.isdir(hip) is False:
                            os.makedirs(hip)
                            os.makedirs(hiplight)
                        elif os.path.isdir(hiplight) is False:
                            os.makedirs(hiplight)
                        if os.path.isdir(lightDir) is False:
                            os.makedirs(lightDir)
                        
                        #Copy File to HSITE   
                        global overwrite
                        if overwrite:  
                            if not s.startswith("op:/"):
                                if not copy(s, lightDir):
                                    continue
                        else:
                            if os.path.exists(hou.getenv("HSITE") + "/" + project + "/" + hipname + "/" + light + "/" + n.name() + "/" + filename):
                                continue    
                            elif not copy(s, lightDir):
                                continue

                        newPath = "$HSITE/" + project + "/" + hipname + "/" + light + "/" + n.name() + "/" + filename
                        #newPath to Parm
                        n.parm(p.name()).set(newPath)
                        count += 1
    return count

def copy(s, dest):
    try:
        shutil.copy(s, dest)
    except IOError, arg:
        ex = s + ": "+ arg[1]
        errors.append(ex)
        return False
    return True

def printErrors(text):

    text = text + "Errors: \n"
    msg = ""
    for s in errors:
        msg = msg + s + "\n"

    text = text + msg
    return text
