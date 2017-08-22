#####################################
#LICENSE                            #
#####################################
#
# Based and adapted from  Niklas Rosenstein
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
This script increments the number at the end of the current scene's name and
saves it as a new file. If there is no number at the end, it will append a
new number suffix and start from "1".  It also will add the current Date in
reverse form (YYMMDD) to the Filename as a prefix.

If the EnvironmentVariable DEFAULTJOBwas set via HOUDINI.ENV it will recognize
if a project was set already and will ask for one if not.
DEFAULTJOB has to point to Houdini´s Default Project location, eg. C:/Users/Elmar Glaubauf

There is also a Mask for the filename based on the structure 'scene_shotname_version_variant'
(eg.: sc01_sh020_50_A). It can be easily modified via the shotname variable below

If a file is saved it will check for the subdirectories created when Houdini creates
a project. Additionally it creates some other folders (editable below) by default.

Feel free to comment/edit/contact me for further development.
Currently only tested on Windows

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import hou
import os
import re
import datetime

#################################
#CONFIGURATION
#################################
#Directories to be created
directories = ["geo", "hda", "sim", "abc", "tex", "render", "flip", "scripts", "comp", "audio", "video", "desk", "clips", "images", "in", "out", "tmp--sim", "_old", "flipbook" ]
new_suffix_format = '_001'
#Markers Between Filename Input
shotName = ["sc", "_sh", "_", "_"]

#UI
labels = ["Scene (scXX)", "Shot1 (shXXX)", "Shot2 (_XX_)", "Variant (_A)"]
buttons = ["Ok", "Cancel"]

#######################################
#CONFIGURATION END
#######################################


    ##############################
    #Check if file already exists and Save
    ##############################
def save(filename):
    if os.path.isfile(filename):
        overwrite = hou.ui.displayConfirmation(
            'The file "{}" already exists. Do you want to overwrite it?' .format(filename))
        if not overwrite:
            return
    #Save
    hou.hipFile.save(filename)
    return()

    ###################
    # Create Missing Project Dirs
    ####################
def makeDirs(projDir):
    for dir in directories:
        dir = projDir + dir
        if not os.path.exists(dir):
            os.makedirs(dir)
    return()

    ####################
    # Get License Info
    ####################
def getLicenseType():
    if hou.licenseCategory() == hou.licenseCategoryType.Indie:
        return ".hiplc"
    elif hou.licenseCategory() == hou.licenseCategoryType.Commercial:
        return ".hip"
    else:
        return ".hipnc"


    #################################################
    # Create and set new Folder Structure and Project
    #################################################
def setProj(base):
    invalid = True
    while invalid:
        userdir = hou.ui.selectFile(title="Please choose a Project Directory", collapse_sequences = True, file_type = hou.fileType.Directory)
        #Search for ENVVARS
        reg = re.compile('(\${1})([A-Z]+)')
        match = reg.search(userdir)
        if match:
            first, second = match.groups()

            myPath = hou.getenv(second)
            length = len(second)+1
            #Replace Them
            userdir = myPath + userdir[length:]

        if os.path.isdir(userdir):
            invalid = False
            #Create Direcotries
            ud = userdir
            makeDirs(userdir)
            userdir = userdir + base
        else:
            hou.ui.displayMessage("Please select a directory")
    hou.putenv("JOB", userdir)
    return ud

    ###############################
    #Increment Versionnumber by one
    ###############################
def increaseVersionNum(basename):
    regex = re.compile('(.*)(\d{1,})(\.\w+)')
    match = regex.match(basename)

    if match:
        basename, number, ext = match.groups()
        basename += str(int(number) + 1).rjust(len(number), '0') + ext
    else:
        ext = getLicenseType()
        basename += new_suffix_format + ext
    return basename

    #############################################
    #Add Date if not existing in basename already
    #############################################
def addDate(basename):
    today = datetime.date.today().strftime("%y%m%d")
    #Starts with number?
    regDate = re.compile('^[0-9]{6}')
    match = regDate.match(basename)
    if match:
        #check if current date
        regDate = basename[:6]
        if today != regDate:
            basename = basename[6:]
            if basename[0] == "_":
                basename = today + basename
            else:
                basename = today + "_" + basename
    else:
        #add current date in front
        basename = today + "_" + basename
    return basename

    ########################################
    #Get Completely New FileStructure & Name
    ########################################
def getNewFile():
    invalid = True
    while invalid:
       invalid = False
       newName = hou.ui.readMultiInput("Please Insert New File Name", labels, buttons = buttons, default_choice = 0, close_choice = 1, title="Choose Filename")
       for elem in newName[1]:
             elem.replace(" ", "")
             if elem == "":
                invalid = True
       if newName[0] == 1:
            invalid = False

    # Apply new Name if valid
    if newName[0] != 1:
        basename = shotName[0] + newName[1][0] + shotName[1] + newName[1][1] + shotName[2] + newName[1][2] + shotName[3] + newName[1][3]

        #Add Date to Basename
        basename = addDate(basename)
        #Increase Version
        basename = increaseVersionNum(basename)
        #Set Proj
        ud = setProj(basename)
        #Full Filename
        filename = ud + basename
        save(filename)

    ########################################
    #Get Data from Existing File and Iterate
    #########################################
def getDatafromCurrentFile():
    if hou.getenv("DEFAULTJOB") == hou.getenv("JOB"):
        getNewFile()
    else:
        #Get Data from Current File
        hip = hou.hipFile
        filename = hip.path()
        basename = hip.basename()
        pathname = re.sub(basename+"$", '', filename)

        #Correct Date if necessary
        basename = addDate(basename)
        #Increase Version
        basename = increaseVersionNum(basename)
        #Concat again
        filename = pathname + basename
        #Save
        save(filename)


    #################################
    #Main Call
    ################################
def main():

    useCF = hou.ui.displayMessage("Use current Project/Filename?", buttons=('Yes', 'No'), title = "Use current File?")
    if not useCF:
        getDatafromCurrentFile()
    else:
        getNewFile()


main()
