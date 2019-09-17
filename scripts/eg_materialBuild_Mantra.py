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

TODO: Enable optional Texture conversion to .rat/rs
"""



import re
import hou
import os
import shutil

extension = ".rat"
#Context
obj = hou.node("/obj")
mat = hou.node("/mat")

#StringHolders
base_color = ""
roughness = ""
normal = ""
metallic = ""
reflect = ""
displace = ""
bump = ""
ao = ""
uv = ""


#vars
img = ""
mb = ""
username = ""
pc = ""

def run():

    getFiles()
    getName()
    createMaterial()
    
def createMaterial():


    #Create Base
    global mb
    global base_color
    global roughness
    global normal
    global metallic
    global reflect
    global bump
    global displace
    global ao
    global uv

    mb = mat.createNode("materialbuilder")
    mb.setName(username, True)
    mb.moveToGoodPosition()
    
    #Get Surface Output Node
    so = mb.glob("surface_output")[0]
    
    se = mb.createNode("surfaceexports")
    
    so.setInput(0, se, 0)
    so.setInput(1, se, 1)
    so.setInput(4, se, 2)
        
    #Create PrincipledShader
    global pc
    pc = mb.createNode("principledshader")

    #Layer Export
    layer = mb.createNode("parameter")
    layer.parm("parmname").set("layer")
    layer.parm("exportparm").set(1)
    layer.parm("useownexportcontext").set(1)
    layer.parm("parmtype").set("struct")
    layer.parm("parmtypename").set("ShaderLayer")
    layer.setInput(0,pc,2)

    se.setInput(0, pc, 2)

    
    uv = mb.createNode("uvcoords::2.0")
        
    #################
    ######Layers#####
    #################
    if base_color is not "":
        base_color = convertFiles(base_color, 0)
        createTexture(base_color, "Base_Color")
        if ao is not "":
            ao = convertFiles(ao, 1)
            createTexture(ao, "Ambient_Occlusion")
    if roughness is not "":
        roughness = convertFiles(roughness, 1)
        createTexture(roughness, "Roughness")
    if metallic is not "":
        metallic = convertFiles(metallic, 1)
        createTexture(metallic, "Metallic")
    if reflect is not "":
        reflect = convertFiles(reflect, 1)
        createTexture(reflect, "Reflectivity")
    if normal is not "":
        normal = convertFiles(normal, 1)
        createNormal(normal, "Normal")  
    if displace is not "":
        displace = convertFiles(displace, 1)
        createDisplace(displace,"Displace")
    if bump is not "":
        bump = convertFiles(bump, 1)
        createNormal(bump, "Bump")     

    mb.layoutChildren()
    
    return

def createTexture(channel, channelName):
    
    global uv

    tex = mb.createNode("texture::2.0")
    tex.setName(channelName, True)
    tex.parm("map").set(channel)

    tex.setInput(0, uv, 0)

    #################
    ###Layers####
    #################
    if channelName is "Base_Color":
     pc.setNamedInput("basecolor", tex, 0)
    elif channelName is "Roughness":
     pc.setNamedInput("rough",tex, 0)
    elif channelName is "Metallic":
     pc.setNamedInput("metallic",tex, 0)
    elif channelName is "Reflectivity":
     pc.setNamedInput("reflect",tex, 0)
    elif channelName is "Ambient_Occlusion":
        mult = mb.createNode("multiply")
        pc.setNamedInput("basecolor", mult, 0)
        
        bc = mb.glob("Base_Color")[0]
        mult.setInput(0, bc, 0)
        mult.setInput(1, tex,0)
    return

def createNormal(channel, channelName):
    global uv

    tex = mb.createNode("displacetexture")
    tex.setName(channelName, True)
    tex.parm("texture").set(channel)  
    tex.setInput(2, uv, 0)
    if channelName is "Normal":
        tex.parm("type").set("normal")
    elif channelName is "Bump":
        tex.parm("type").set("bump")
        tex.parm("scale").set(0.01)
    
    pc.setNamedInput("baseN",tex, 1)

    return

def createDisplace(channel, channelName):

    global uv
    
    tex = mb.createNode("displacetexture")
    tex.setName(channelName, True)
    tex.parm("texture").set(channel)  
    tex.parm("scale").set("0.1")
    tex.setInput(2, uv, 0)

    mb.glob("displacement_output")[0].setInput(0,tex, 0)
    mb.glob("displacement_output")[0].setInput(1,tex, 1)

    #Create Properties
    prop = mb.createNode("properties")

    #Add Template Parm
    group = prop.parmTemplateGroup()
    folder = hou.FolderParmTemplate("folder", "Shading")
    folder.addParmTemplate(hou.FloatParmTemplate("vm_displacebound", "Displacement Bound", 1))
    group.append(folder)    
    prop.setParmTemplateGroup(group)
    prop.parm("vm_displacebound").set(1)
    

    #Connect
    mb.glob("*collect")[0].setInput(2,prop,0)

    #Layer Export
    lp = mb.createNode("layerpack")
    lp.setInput(3, tex, 0)
    lp.setInput(4, tex, 1)

    
    layer = mb.createNode("parameter")
    layer.parm("parmname").set("layer")
    layer.parm("exportparm").set(1)
    layer.parm("useownexportcontext").set(1)
    layer.parm("exportcontext").set("displace")
    layer.parm("parmtype").set("struct")
    layer.parm("parmtypename").set("shaderlayer")

    layer.setInput(0,lp, 0)

    return


def convertFiles(channel, linear):

    cop = hou.node("/img")
    img = cop.createNode("img", "tmp")


    
    read = img.createNode("file")
    #Set ColorSpace
    if linear == 1:
        read.parm("colorspace").set("linear")
    else:
        read.parm("colorspace").set("srgb")

    rop = img.createNode("rop_comp")
    rop.setInput(0,read,0)
    rop.parm("trange").set(0)

    #Convert Stuff
    read.parm("filename1").set(channel)
    
    #Change Filename
    namePos = channel.rfind(".")
    name = channel[:namePos]
    name += extension
    
    
    #Render
    rop.parm("copoutput").set(name)
    rop.parm("execute").pressButton()
    
    #Cleanup
    img.destroy()

    #Return new Filename to Caller
    return name


def getName():

    #Make InputField
    global username
    username = hou.ui.readInput("Call me Names", title="Name")[1]
    if username is "":
           exit()
    #Remove Special Chars and replace them with "_"
    for k in username.split("\n"):
        username = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
    username = username.replace(" ", "_")
    
    
    
def getFiles():
    files = hou.ui.selectFile(title="Please choose Files to create a Material from", collapse_sequences = False, multiple_select = True, file_type = hou.fileType.Image)
    if files is "":
           exit()
    strings = files.split(";")
    
    global base_color
    global roughness
    global normal
    global metallic
    global reflect
    global bump
    global displace
    global ao

       
    for i, s in enumerate(strings):
        s = s.rstrip(' ')
        s = s.lstrip(' ')
        
        #Get Name of File
        name = s.split(".")
        k = name[0].rfind("/")
        name = name[0][k+1:]
    
    
        
        if "base_color" in name.lower() or "basecolor" in name.lower():
            base_color = s
        elif "roughness" in name.lower():
            roughness = s
        elif "normal" in name.lower():
            normal = s
        elif "metallic" in name.lower():
            metallic = s
        elif "reflect" in name.lower():
            reflect = s
        elif "height" in name.lower():
            displace = s
        elif "displace" in name.lower():
            displace = s
        elif "bump" in name.lower():
            bump = s
        elif "ao" in name.lower() or "ambient_occlusion" in name:
            ao = s
     
    return

