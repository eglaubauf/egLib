# egLib

A collection of scripts for SideFx Houdini - Python3

## Provided Scripts

- MatchTransforms - Aligns Nodes to each other - based on transforms
- Autofocus - Creates a camera with autofocus set up
- FlipBook - Creates a flipbook from the current camera without cropping/scaling
- IncrementalSave- save with date, name, version - iterates version on each save
- makeQCam   - make a cam with QFrustum and QRig - needs qLib
- measure - make a measure node from selected objects - if non selected create nulls instead
- multiImporter - import multiple files (.bgeo, .abc, .fbx,...) into OBJ - Creates a OBJ_node with names for each selected file
- StringReplace - search ALL nodes in the scene for referenced Files - Provides a list view - to choose which to replace
- resetTrans - reset transforms to zero (Components selectable) - OBJ
- trajectory - create a visible trajectory for the selected object (OBJ) - needs Qlib installed

## Provided HDAs

- AtomArray.hdalc - As know from other DCCs
- AutoUV_LowToHigh.hdalc -  AutoUVs the LowRes Object and transfers UVs from Low to HighPoly - (SideFx)GameDev Logic inside
- compressvdb.hdalc - save space with VDBs
- compressvolume.hdalc - save space with volumes and VDBs
- deleteOutsidePieces.hdalc - delete pieces which are not on the inside
- EdgeDisplacement.hdalc - Displaces Edges
- HexGrid - Creates a Flat Hexagonal Grid
- PolyCapFix - Fixes Holes
- Project - sets a few environment Variables which are handy if you have a bigger Project, provides incremental Saves
- sourcePyro - Source Pyro Nodes packaged up
- VolumeDisplacement.hdalc - Does VolumeDisplacement (in SOP/VOPs on VDBs)
- VoronoiTransform.hdalc - Breaks things and Transforms Pieces

## deprecated HDAs (development stopped):
- FileCache - now supported by vanilla houdini
- Noise to Volume - The pre H18 way - not needed

## Support

- Tested with Houdini 19.5.334 on Ubuntu 22.04

## Installation:

Copy the Provided egLib.json to your houdini user Directory within the packages folder:

```/home/<user>/houdini19.0/packages```

Change the below line according to where you downloaded the git-Repository:

```"EGLIB": "/home/<user>/git/egLib"```


## Notes:

All of the scripts are free of charge for free use, commercial or non commercial whatsoever.
If you find issues please report.
