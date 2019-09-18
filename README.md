# egLib

A collection of scripts for SideFx Houdini - free for all purposes

### Features:

#### Provided Scripts
This library provides a set of Scripts:

- autofocus.py - does as it says
- connectPoints.py - connects polyPoints
- flipBook.py - makes a Flipbook from the current camera without croppin/scaling
- hide.py - toggles hide afrom selected nodes from viewport
- IN.py - Green Null with handy rename panel provides; appends to selected node (SOP), shortcut recommended
- incrSave.py - save with date, name, version - iterates version(if necessary also date) on each save
- makePlanarX.py - Flattens pointSelection in World X
- makePlanarY.py - Flattens pointSelection in World Y
- makePlanarZ.py - Flattens pointSelection in World Z
- makeQCam.py   - make a cam with Frustum - needs qLib
- measure.py - make a measure node from selected objects - if non selected create nulls instead
- merge.py - merge selected with merge node (SOP) - Shortcut highly recommended (M works fine)
- multiImporter.py - import multiple files (.bgeo, .abc, .fbx,...) into OBJ - Creates a OBJ_node with names for each selected file
- out.py - Black Null with handy rename panel provides; appends to selected node (SOP); shortcut recommended
- replaceString.py - search ALL nodes in the scene for all string-parms and replace a string if found
- resetTrans.py - reset Transforms to zero (Components selectable) - OBJ
- trajectory.py - create a visible trajectory for the selected object (OBJ) - needs Qlib installed
- align.py  - align 2 nodes in OBJ

#### Provided HDAs


- PolyCapFix - Fixes Holes
- VolumeDisplacement.hdalc - Does VolumeDisplacement
- VoronoiTransform.hdalc - Breaks things and Transforms Pieces
- AtomArray.hdalc - As it says
- compressvdb.hdalc - save space with vdbs
- compressvolume.hdalc - save space with vdbs
- DeleteOutsidePieces.hdalc - delete pieces which are not on the inside
- DigitalGrowth2D.hdalc - Line-Growth Solver
- EdgeDisplacement.hdalc - EdgeDisplacement (PolyEdges)
- LineGlow.hdalc - Shader
- MacBethMantra.hdalc - a MacBethChart for Mantra
- MoGraph_Shader - MoGraphStuff as known from other tools
- MoGraph_Step - MoGraphStuff as known from other tools
- MoGraph_Target - MoGraphStuff as known from other tools
- Mograph_Displace.hda - MoGraphStuff as known from other tools
- Mograph_Plain.hda - MoGraphStuff as known from other tools
- Mograph_Random.hda - MoGraphStuff as known from other tools

### additional Infos

- Toolbar provided 
- Icons may follow
- Tested on 17.5.360 
- If you find any bugs, have suggestions or anything else please contact me via Twitter or per Mail
- please check out my other Repos as well - they might be handy to you


### Installation:

Append egLib to Houdini Python path or add to 123.py or 456.py

```
import sys
sys.path.append("<PathToLib>\scripts")
```

For enabling the HDAs your Houdini.env needs to be extended (add this line to your houdini.env):

```
HOUDINI_OTLSCAN_PATH=$HOUDINI_OTLSCAN_PATH;<pathToEgLib>\otls;&
```

### Notes:

All of the scripts are free of charge for free use, commercial or non commercial whatsoever.  Individual Licenses are added to each file as some of these are based on work done by other devs and shall be included in branches, adaptions of this scripts. Anyone is allowed to modify, develop, change the files for his/her purpose.

The Scripts in the scripts Folder shall be added as tools to a custom Toolbar. Linking them with some keyboard shortcuts is recommended.


### Contact/Issues/Features/Questions

For any questions and/or improvement suggestions just contact me via twitter or mail.<br>
Twitter: @eglaubauf <br>
Web: www.elmar-glaubauf.at
