# egLib
#A collection of scripts for SideFx Houdini

### Features:



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

Some of the Files need a modified HOUDINI.ENV. An Example File is provided in the prefs Folder. I try to remove the dependencies to Houdini.env. 

The Scripts in the scripts Folder shall be added as tools to a custom Toolbar. Linking them with some keyboard shortcuts is recommended.


For any questions and/or improvement suggestions just contact me via twitter or mail.<br>
Twitter: @eglaubauf <br>
Web: www.elmar-glaubauf.at
