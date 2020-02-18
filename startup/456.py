import sys 
sys.path.append("D:\Git\egLib\scripts")
sys.path.append("D:\Git\Houdini_CopyToFarm")
sys.path.append("D:\Git\materialBuildMantra\scripts")
sys.path.append("D:\Git\materialBuildRedshift\scripts")

#Set DefaultShape & Color Redshift Lights
hou.nodeType(hou.objNodeTypeCategory(), "rslight").setDefaultColor(hou.Color(1,1,0))
hou.nodeType(hou.objNodeTypeCategory(), "rslight").setDefaultShape('light')

hou.nodeType(hou.objNodeTypeCategory(), "rslighties").setDefaultColor(hou.Color(1,1,0))
hou.nodeType(hou.objNodeTypeCategory(), "rslighties").setDefaultShape('light')

hou.nodeType(hou.objNodeTypeCategory(), "rslightportal").setDefaultColor(hou.Color(1,1,0))
hou.nodeType(hou.objNodeTypeCategory(), "rslightportal").setDefaultShape('light')

hou.nodeType(hou.objNodeTypeCategory(), "rslightsun").setDefaultColor(hou.Color(1,1,0))
hou.nodeType(hou.objNodeTypeCategory(), "rslightsun").setDefaultShape('light')

hou.nodeType(hou.objNodeTypeCategory(), "rslightdome::2.0").setDefaultColor(hou.Color(1,1,0))
hou.nodeType(hou.objNodeTypeCategory(), "rslightdome::2.0").setDefaultShape('light')