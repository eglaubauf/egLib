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
new_suffix_format = '_001'
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
    #Get Data from Existing File and Iterate
    #########################################
def getDatafromCurrentFile():
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

    getDatafromCurrentFile()

main()
