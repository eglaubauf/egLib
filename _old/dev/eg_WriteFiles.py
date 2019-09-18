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
This script searches FileNodes for a pattern writes out bgeo files and loads them back in

TODO: UI

Twitter: @eglaubauf 
Web: www.elmar-glaubauf.at
"""

import hou

def run():

    obj = hou.selectedNodes()



    search_A = 'BaseStones'
    search_B = 'BaseStone'
    newString_A = 'opdef:/Object/MAPRO_Landscape_V3_?LandscapeStones.fbx'
    newString_B = 'opdef:/Object/MAPRO_Landscape_V3_?BaseStones.fbx'
    visited = []
    view = 0

    for n in obj:
            if n not in visited:
            for inner in n.children():
                if inner.isGenericFlagSet(hou.nodeFlag.Display):
                    view = inner
            for inner in n.children():
                if inner.type().name() == "file":
                    
                    s = inner.parm('file').evalAsString()
                    
                    f = n.createNode('filecache')
                    f.setNextInput(inner)
                    f.setDisplayFlag(True)
                    f.setRenderFlag(True)
                    f.moveToGoodPosition()
                    f.parm('trange').set(0)
        
                    s1 = s[:s.index(".")]
                    s2 = s[s.index("#"):]
                                
                    s2 = s2[1:s2.index(",")]
                
                    
                    s = s1 + '_' + s2 + '.bgeo'
                    f.parm('file').set(s)
                    
                    f.parm('execute').pressButton()
                    
                    if inner.isGenericFlagSet(hou.nodeFlag.Lock):
                        inner.setGenericFlag(hou.nodeFlag.Lock, False)
                    
                    inner.parm('file').set(s)
                    f.destroy()
            
                
            view.setGenericFlag(hou.nodeFlag.Display, True)
            view.setGenericFlag(hou.nodeFlag.Render, True)                 
            visited.append(n)
            
    print "Done"