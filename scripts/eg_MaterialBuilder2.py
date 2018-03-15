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
This script will build a Material Tree based on a File Selection 
The Files are parsed for the Terms "Base_Color", "Metallic", "Roughness", "Reflectivity" and "Normal"
The Node Tree will be built within a Materialbuilder. Textures will be wired into a properly named COPs Network and linked back in with Relative Paths . 
Easy transfer to a Farm is possible with this technique. 

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""


import re
import hou
import os

#Context
obj = hou.node("/obj")
cop = hou.node("/img")
mat = hou.node("/mat")

#StringHolders
base_color = ""
roughness = ""
normal = ""
metallic = ""
reflect = ""

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
    mb = mat.createNode("materialbuilder")
    mb.setName(username, True)
    mb.moveToGoodPosition()
    
    print mb.children()
    #Get Surface Output Node
    so = mb.glob("surface_output")[0]
    
    se = mb.createNode("surfaceexports")
    
    so.setInput(0, se, 0)
    so.setInput(1, se, 1)
    so.setInput(4, se, 2)
    
    
    #Create PrincipledShader
    global pc
    pc = mb.createNode("principledshader")

    se.setInput(0, pc, 2)
    #COPS Global
    global img
    img = cop.createNode("img")
    img.setName(username, True)
    img.moveToGoodPosition()
    
    #################
    ###Layers####
    #################
    if base_color is not "":
        createTexture(base_color, "Base_Color")
    if roughness is not "":
        createTexture(roughness, "Roughness")
    if metallic is not "":
        createTexture(metallic, "Metallic")
    if reflect is not "":
        createTexture(reflect, "Reflectivity")
    if normal is not "":
        createNormal(normal, "Normal")        

    
    mb.layoutChildren()
    
    return

def createTexture(channel, channelName):
    
    img_bc = img.createNode("file")
    img_bc.parm("filename1").set(channel)
    img_bc.moveToGoodPosition()

    img_nbc = img.createNode("null")
    img_nbc.setName("OUT_" + channelName.upper())
    
    
    img_nbc.setInput(0, img_bc, 0)
    img_nbc.moveToGoodPosition()
    
    bc = mb.createNode("texture::2.0")
    bc.setName(channelName, True)

    #################
    ###Layers####
    #################
    if channelName is "Base_Color":
     pc.setNamedInput("basecolor", bc, 0)
    elif channelName is "Roughness":
     pc.setNamedInput("rough",bc, 0)
    elif channelName is "Metallic":
     pc.setNamedInput("metallic",bc, 0)
    elif channelName is "Reflectivity":
     pc.setNamedInput("reflect",bc, 0)
    
    p_bc = mb.createNode("parameter")
    p_bc.parm("parmname").set(channelName)
    p_bc.parm("parmlabel").set(channelName)

    #Set Parameter outside
    p_bc.parm("parmtype").set(15)
    bc.setNamedInput("map", p_bc, 0)

    #Connect to COPS
    bc_path = "op:`opfullpath('"+ bc.parent().relativePathTo(img_nbc) + "')`"     
    mb.parm(channelName).set(bc_path)

    return

def createNormal(channel, channelName):
    
    img_bc = img.createNode("file")
    img_bc.parm("filename1").set(channel)
    
    img_nbc = img.createNode("null")
    img_nbc.setName("OUT_" + channelName.upper())
    
    img_nbc.setInput(0, img_bc, 0)
    
    bc = mb.createNode("displacetexture")
    bc.setName(channelName, True)

    pc.setNamedInput("baseN", bc, 1)

    p_bc = mb.createNode("parameter")
    p_bc.parm("parmname").set(channelName)
    p_bc.parm("parmlabel").set(channelName)

    #Set Parameter outside
    p_bc.parm("parmtype").set(15)
    bc.setNamedInput("texture", p_bc, 0)

    #Connect to COPS
    bc_path = "op:`opfullpath('"+ bc.parent().relativePathTo(img_nbc) + "')`"     
    mb.parm(channelName).set(bc_path)

    return

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

       
    for i, s in enumerate(strings):
         s = s.rstrip(' ')
         s = s.lstrip(' ')
         
         #Get Name of File
         name = s.split(".")
         k = name[0].rfind("/")
         name = name[0][k+1:]
        
        
            
         if "base_color" in name.lower():
            base_color = s
         elif "roughness" in name.lower():
            roughness = s
         elif "normal" in name.lower():
            normal = s
         elif "metallic" in name.lower():
            metallic = s
         elif "reflect" in name.lower():
            reflect = s
     
    return

