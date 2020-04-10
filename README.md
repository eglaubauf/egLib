# egLib

A collection of scripts for SideFx Houdini

## Provided Scripts

- align - Aligns Nodes to each other - based on transforms
- autofocus - does as it says
- flipBook - makes a Flipbook from the current camera without croppin/scaling
- hide- toggles hide afrom selected nodes from viewport
- in - Green Null with handy rename panel provided; appends to selected node (SOP), shortcut recommended
- incrSave- save with date, name, version - iterates version(if necessary also date) on each save
- isolate - isolates the selection - (hides everything else)
- makePlanarX - Flattens pointSelection in World X
- makePlanarY - Flattens pointSelection in World Y
- makePlanarZ - Flattens pointSelection in World Z
- makeQCam   - make a cam with QFrustum and QRig - needs qLib
- measure - make a measure node from selected objects - if non selected create nulls instead
- merge - merge selected with merge node (SOP) - Shortcut highly recommended (M works fine)
- multiImporter - import multiple files (.bgeo, .abc, .fbx,...) into OBJ - Creates a OBJ_node with names for each selected file
- out - Black Null with handy rename panel provided; appends to selected node (SOP); shortcut recommended
- StringReplace - search ALL nodes in the scene for referenced Files - Provides a list view - to choose which to replace
- resetTrans - reset Transforms to zero (Components selectable) - OBJ
- showAll - unhides all Nodes in the secene
- trajectory - create a visible trajectory for the selected object (OBJ) - needs Qlib installed

## Provided HDAs

- AtomArray.hdalc - As know from other DCCs
- AutoUV_LowToHigh.hdalc -  AutoUVs the LowRes Object and transfers UVs from Low to HighPoly - (SideFx)GameDev Logic inside
- compressvdb.hdalc - save space with vdbs
- compressvolume.hdalc - save space with volumes
- DeleteOutsidePieces.hdalc - delete pieces which are not on the inside
- DigitalGrowth2D.hdalc - Line-Growth Solver
- EdgeDisplacement.hdalc - Displaces Edges
- TOPs Flipbook - Flipbook Generator based on TOPS - als renders a video (with ffmpeg) to $HIP/videos
- FileCache - enables writing of filecaches, based on Enviroment Variables set by the Project Node, also has the ability to move Caches from within Houdini do a different directory
- HexGrid - Creates a Flat Hexagonal Grid
- Mograph_Displace.hda - MoGraphStuff as known from other tools
- Mograph_Plain.hda - MoGraphStuff as known from other tools
- Mograph_Random.hda - MoGraphStuff as known from other tools
- MoGraph_Shader - MoGraphStuff as known from other tools
- MoGraph_Step - MoGraphStuff as known from other tools
- MoGraph_Target - MoGraphStuff as known from other tools
- PolyCapFix - Fixes Holes
- Project - sets a few environment Variables which are handy if you have a bigger Project
- SmoothGeo - Smoothing of Geometry in a few different ways
- VolumeDisplacement.hdalc - Does VolumeDisplacement (in SOP/VOPs on VDBs)
- VoronoiTransform.hdalc - Breaks things and Transforms Pieces

## additional Infos

- easy Usage a provided shelf
- provides error messages if required Libraries are missing
- easy Install via Packages Workflow - see more below
- Tested on Houdini 18.0.391
- Tested on Windows 10 and Linux (Ubuntu 19.10)
- Open Source - Feel free to branch or fork

## Installation:

Copy the Provided egLib.json to your houdini user Directory within the packages folder:

```/home/<user>/houdini18.0/packages```

Change the below line according to where you downloaded the git-Repository:

```"EGLIB": "/home/elmar/git/egLib"```


## Notes:

All of the scripts are free of charge for free use, commercial or non commercial whatsoever.

## Contact/Issues/Features/Questions

If you find any bugs, have suggestions or anything else please open Issues or contact me via twitter or mail. Please check out my other Repos as well, they might be handy to you.


Twitter: @eglaubauf <br>
Web: www.elmar-glaubauf.at
