# egLib

A collection of scripts for SideFx Houdini

## Provided Scripts

- autofocus.py - does as it says
- connectPoints.py - connects polyPoints
- flipBook.py - makes a Flipbook from the current camera without croppin/scaling
- hide.py - toggles hide afrom selected nodes from viewport
- IN.py - Green Null with handy rename panel provided; appends to selected node (SOP), shortcut recommended
- incrSave.py - save with date, name, version - iterates version(if necessary also date) on each save
- makePlanarX.py - Flattens pointSelection in World X
- makePlanarY.py - Flattens pointSelection in World Y
- makePlanarZ.py - Flattens pointSelection in World Z
- makeQCam.py   - make a cam with QFrustum and QRig - needs qLib
- measure.py - make a measure node from selected objects - if non selected create nulls instead
- merge.py - merge selected with merge node (SOP) - Shortcut highly recommended (M works fine)
- multiImporter.py - import multiple files (.bgeo, .abc, .fbx,...) into OBJ - Creates a OBJ_node with names for each selected file
- out.py - Black Null with handy rename panel provided; appends to selected node (SOP); shortcut recommended
- replaceString.py - search ALL nodes in the scene for all string-parms and replace a string if found
- resetTrans.py - reset Transforms to zero (Components selectable) - OBJ
- trajectory.py - create a visible trajectory for the selected object (OBJ) - needs Qlib installed
- align.py  - matches transform of 2 nodes in OBJ

## Provided HDAs

- HexGrid - Creates a Hexagonal Grid
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
- MacBethRedshift.hdalc - a MacBethChart for Redshift
- MoGraph_Shader - MoGraphStuff as known from other tools
- MoGraph_Step - MoGraphStuff as known from other tools
- MoGraph_Target - MoGraphStuff as known from other tools
- Mograph_Displace.hda - MoGraphStuff as known from other tools
- Mograph_Plain.hda - MoGraphStuff as known from other tools
- Mograph_Random.hda - MoGraphStuff as known from other tools
- AutoUV_LowToHigh.hdalc -  AutoUVs the LowRes Object and transfers UVs from Low to HighPoly - (SideFx)GameDev Logic inside

## additional Infos

- Toolbar provided
- The Redshift-Functionalities have been removed and will be moved to a separate Repository
- If you find any bugs, have suggestions or anything else please contact me via Twitter or per Mail

## Installation

Install via Houdini-Packages Workflow:
    - Copy to provided egLib.json File to your houdini18.0 directory
    - Configure the path for $EGLIB within the file to the location of the downloaded directory
    - enjoy

## Notes

All of the scripts are free of charge for free use, commercial or non commercial whatsoever.  Individual Licenses are added to each file as some of these are based on work done by other devs and shall be included in branches, adaptions of this scripts. Anyone is allowed to modify, develop, change the files for his/her/their purpose.

## Contact/Issues/Features/Questions

If you find any bugs, have suggestions or anything else please open an issue. For any questions and/or improvement suggestions feel free contact me via twitter or mail.

Twitter: @eglaubauf  
web: www.elmar-glaubauf.at
