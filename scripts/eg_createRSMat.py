#####################################
#  LICENSE                            #
#####################################
#
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
"""
This script will create a Redshift Node Network based on a file selection

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""
import hou


class RSMat():
    """Creates an RS-Material in the given context"""
    def __init__(self, context=hou.node("/mat"), name="RedshiftMaterial"):
        self.mat = context
        self.name = name
        self.material_builder = ""
        self.create_material()

    def create_material(self):
        """Creates an RS-Material in the given context"""
        # RS Material Builder
        self.material_builder = self.mat.createNode("redshift_vopnet")
        self.material_builder.setName(self.name, True)
        self.material_builder.moveToGoodPosition()

        # RS Material
        redshift_material = self.material_builder.children()[0]
        rs_mat = self.material_builder.createNode('redshift::Material')
        redshift_material.setInput(0, rs_mat, 0)

    def get_path(self):
        """Returns the Path to the MaterialBuilder"""
        return self.material_builder.path()
        # alternative: relativePathTo(base_node)--> str
