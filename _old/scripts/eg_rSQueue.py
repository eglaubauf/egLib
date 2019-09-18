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
This script will create a simple queue for Rendering with Redshift on a single Machine

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""

#Get Required Stuff

import soptoolutils
import objecttoolutils
import json

def run(kwargs):
    #File Path were RenderFile is
    data_path = "C:/RenderWarrior/lib/data/RenderData.json"
    choices_GPU = ["GTX 1070", "GTX 960"]
    defaultChoices = [0,1]
    renderGPU = ["False", "False"]

    #SELECT GPU DIALOG
    def selectGPU( ):
        selected = 0
        while(selected == 0):
            selectedGPU = hou.ui.selectFromList( choices_GPU , default_choices = defaultChoices, message="Select GPU for Rendering", num_visible_rows=1)
            if len(selectedGPU) != 0:
                #Get Data out of Tuple
                for elem in selectedGPU:
                    if elem == 0:
                        renderGPU[0] = "True"
                    if elem == 1:
                        renderGPU[1] = "True"
                selected = 1
        return


    #Get Selected Nodes
    selNodes = hou.selectedNodes()
    version = hou.applicationVersionString()

    if len(selNodes) != 0:
        #Current ROP Node
        currROP = selNodes[0]
        #Check if Node is a Redshift ROP Node
        success = currROP.name().find("Redshift_ROP")
        if success == -1 :
            msg = ["Okay"]
            hou.ui.displayMessage("Please Select a Redshift ROP Node", msg, severity=hou.severityType.Message)
        #Else go On
        else:
                #Create Dialog for GPU Selection
                selectGPU()
                #################################
                #GET existing JSON_DATA
                with open('C:\RenderWarrior\lib\data\RenderData.json') as data_file:
                    data = json.load(data_file)

                #GET Ammount of entries
                length = str(len(data)+1)
                currFile = hou.hipFile.path()

                ###################################
                #Get Data Together
                newData = {"ID": length , "Application": "Houdini_16" , "StartFrame": currROP.parm('f1').evalAsString() , "EndFrame": currROP.parm("f2").evalAsString(), "Increment": currROP.parm('f3').evalAsString(),  "File": currFile,
                "ROP": currROP.name(), "isRendered" : "False", "GPU1" : renderGPU[0], "GPU2" : renderGPU[1] }

                #Update Existing
                data.append(newData)
                #Write
                with open(data_path, 'w') as outfile:
                    json.dump(data, outfile, indent=4)

    else:
        msg = ["Okay"]
        hou.ui.displayMessage(" No Node Selected. Please Select a ROP Node", msg , severity=hou.severityType.Message)
