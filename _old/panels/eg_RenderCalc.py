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
This script creates a Houdini Panel where Rendertime can be calculated within Houdini.
This is more of an experiment for future UI scripting, but could be useful for someone.
It has to be added to the Pyton Panel Editor as a new interface and then can be used as
a tab within Houdini Windows.

Feel free to comment/edit/contact me for further development.
Currently only tested on Windows

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
from PySide2 import QtCore
from PySide2 import QtWidgets
import re

class RenderCalc(QtWidgets.QWidget):
    def createInsertBoxes(self):
        #Create new Widget with GridLayout
        insert = QtWidgets.QGroupBox("Inputs")
        insertLayout = QtWidgets.QGridLayout()

        #Frames
        nframes = QtWidgets.QLabel('Number of Frames')
        insertLayout.addWidget(nframes, 1, 1)
        self.frames = QtWidgets.QLineEdit()
        insertLayout.addWidget(self.frames, 1, 2)

        #Time UI Mins
        mins = QtWidgets.QLabel('Minutes')
        insertLayout.addWidget(mins, 2, 1, 0)
        self.minutes = QtWidgets.QLineEdit()
        insertLayout.addWidget(self.minutes, 2, 2)

        #Time UI Secs
        secs = QtWidgets.QLabel('Seconds')
        insertLayout.addWidget(secs, 3, 1, 0)
        self.seconds = QtWidgets.QLineEdit()
        insertLayout.addWidget(self.seconds, 3, 2)

        #Set Layout of this section
        insert.setLayout(insertLayout)
        return insert

    def createResultBoxes(self):

        result = QtWidgets.QGroupBox("Results")
        resultLayout = QtWidgets.QGridLayout()

        #ResultUI
        self.res = QtWidgets.QLabel('Result', self)

        resultLayout.addWidget(self.res, 1, 2)
        self.res.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        result.setLayout(resultLayout)
        return result


    def calc(self):
        frames = self.frames.displayText()
        if frames == "":
            frames = 0
        else:
            frames = int(re.search(r'\d+', frames).group())

        mins = self.minutes.displayText()
        if mins == "":
            mins = 0
        else:
            mins = int(re.search(r'\d+', mins).group())


        secs = self.seconds.displayText()
        if secs == "":
            secs = 0
        else:
            secs = int(re.search(r'\d+', secs).group())

        #Res in Seconds
        res = (secs + mins*60)*frames
        #Res to
        m, s = divmod(res, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        res = str(d) + " Days " + str(h) + " Hours " + str(m) + " Minutes " + str(s) + " Seconds "


        self.res.setText(res)


    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self,parent)

        mainLayout = QtWidgets.QGridLayout()

        #AddInsertLayout
        mainLayout.addWidget(self.createInsertBoxes(), 1,1)

        #AddResultLayout
        mainLayout.addWidget(self.createResultBoxes(), 2,1)

        #Make Button to Trigger Calculation
        calcB = QtWidgets.QPushButton("Calculate")
        mainLayout.addWidget(calcB,3,1, 1, 1)

        #Button Events
        self.connect(calcB, QtCore.SIGNAL('clicked()'), self.calc)

        #Apply Layout
        mainLayout.setRowMinimumHeight(3,1)
        mainLayout.setSpacing(2)
        self.setLayout(mainLayout)

        # Apply Houdini styling to the main widget.
        self.setProperty("houdiniStyle", True)


#CREATE MAIN INTERFACE
def createInterface():
    calc = RenderCalc()
    return calc
