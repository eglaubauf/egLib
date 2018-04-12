# egLib
#A collection of scripts for SideFx Houdini

### NEW 04/2018

1. Shelves!
2. Fixes (iSaveDate, replaceString)
3. New Scripts!
    - convertToRAT: Scans current HIP for textures in COPS, MAT and OBJ context and converts them to RAT Files - configable in the python Script
    - copyToFarm: Copies all Linked Textures and Geometry to $HSITE and changes the strings - even in locked OTLs as the principled Shaders and so on

When there are problems contact me via Twitter, or raise an Issue on Github. Thank you. 

### NEW 03/2018: 

1. Materialbuilder:
This script will build a Material Tree based on a File Selection 
The Files are parsed for the Terms "Base_Color", "Metallic", "Roughness", "Reflectivity" and "Normal"
The Node Tree will be built within a Materialbuilder. Textures will be wired into a properly named COPs Network and linked back in with Relative Paths . 
Easy transfer to a Farm is possible with this technique. 

2. MultiImporter:
This script will import Geometry Files based on their name into separate Nodes. 
The Geometry is parsed for "Collide" and "Render". Renderfiles can optionially loaded in as Packed Disk Primitives. 
(Selection Dialog)




### Installation:

Append egLib to Houdini Python path or add to 123.py or 456.py

import sys
sys.path.append("<PATHTOLIB>\egLib\scripts")


### Notes:


All of the scripts are free of charge for free use, commercial or non commercial whatsoever.  Individual Licenses are added to each file as some of these are based on work done by other devs and shall be included in branches, adaptions of this scripts. Anyone is allowed to modify, develop, change the files for his/her purpose.

Some of the Files need a modified HOUDINI.ENV. An Example File is provided in the prefs Folder. I try to remove the dependencies to Houdini.env. 

The Scripts in the scripts Folder shall be added as tools to a custom Toolbar. Linking them with some keyboard shortcuts is recommended.


For any questions and/or improvement suggestions just contact me via twitter or mail.<br>
Twitter: @eglaubauf <br>
Web: www.elmar-glaubauf.at
