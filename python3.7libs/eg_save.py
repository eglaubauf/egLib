#####################################
#              LICENSE              #
#####################################
#
# Based and adapted from  Niklas Rosenstein
# Copyright (C) 2020  Elmar Glaubauf
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

"""This script increments the number at the end of the current scene's name and
saves it as a new file. If there is no number at the end, it will append a
new number suffix and start from "1".  It also will add the current Date in
reverse form (YYYYMMDD) to the Filename as a prefix.

Feel free to comment/edit/contact me for further development.
Currently only tested on Windows

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import hou
import os
import re
import datetime

class Save:

    def __init__(self, version=None):

        self.new_suffix_format = '_001'
        self.moveOldFiles = True
        self.oldDir = "versions"
        self.currentVersion = None

        self.get_data_from_file()

    def save(self, filename):
        if os.path.isfile(filename):
            overwrite = hou.ui.displayConfirmation('The file "{}" already exists. Do you want to overwrite it?' .format(filename))
            if not overwrite:
                return
        # Save
        hou.hipFile.save(filename)

    def getLicenseType(self):
        if hou.licenseCategory() == hou.licenseCategoryType.Indie:
            return ".hiplc"
        elif hou.licenseCategory() == hou.licenseCategoryType.Commercial:
            return ".hip"
        else:
            return ".hipnc"

    def getCurrentVersion(self):
        return self.currentVersion

    def setCurrentVersion(self, number):
        self.currentVersion = number

    def increaseVersionNum(self, basename):
        regex = re.compile('(.*)((?<=_)\d+)(\.\w+)')
        match = regex.match(basename)
        if match:
            basename, number, ext = match.groups()
            if number:
                version = str(int(number) + 1).rjust(len(number), '0')
                self.setCurrentVersion(version)
                basename += version + ext
            else:
                basename += self.new_suffix_format + ext
        else:
            regex = re.compile('(.hip)')
            pos = re.search(regex, basename)
            if pos:
                pos = pos.start()
                length = len(basename) - pos
                basename = basename[:-length]
            ext = self.getLicenseType()
            basename += self.new_suffix_format + ext
        self.basename = basename

    def addDate(self, basename):
        today = datetime.date.today().strftime("%y%m%d")
        # Starts with number?
        regDate = re.compile('^[0-9]{6}')
        match = regDate.match(basename)
        if match:
            # check if current date
            regDate = basename[:6]
            if today != regDate:
                basename = basename[6:]
                if basename[0] == "_":
                    basename = today + basename
                else:
                    basename = today + "_" + basename
        else:
            # add current date in front
            basename = today + "_" + basename
        self.basename = basename

    def moveOldFileToDir(self, oldPathname, oldBasename):
        oldpath = oldPathname + oldBasename
        oldFileDir = oldPathname + self.oldDir
        # Skip on frist save
        if not os.path.exists(oldpath):
            return
        if not os.path.exists(oldFileDir):
            os.mkdir(oldFileDir)
        if os.path.isdir(oldFileDir):
            newpath = oldFileDir + "/" + oldBasename
            os.rename(oldpath, newpath)
        return

    def get_data_from_file(self):
        hip = hou.hipFile
        self.filename = hip.path()
        self.basename = hip.basename()
        self.pathname = re.sub(self.basename + "$", '', self.filename)

        # Save Old name for Later
        self.oldPath = self.pathname
        self.oldBasename = self.basename

    def get_path(self):
        return self.pathname

    def incrSave(self):
        # Get Data from Current File
        self.get_data_from_file()

        # Correct Date if necessary
        self.addDate(self.basename)
        # Increase Version
        self.increaseVersionNum(self.basename)

        # Concat again
        self.filename = self.pathname + self.basename

        # Save
        self.save(self.filename)
        if self.moveOldFiles is True:
            self.moveOldFileToDir(self.oldPath, self.oldBasename)
