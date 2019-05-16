import hou
import toolutils

def run():
    sel = hou.selectedNodes()

    if len(sel) == 0:
        raise hou.Error("Nothing was selected")

    for n in sel:
        display = n.displayNode()
        if display:
            geo = display.geometry()
            pivot = n.parmTuple("p").eval()
            sop = n.createNode('xform', 'move_to_pivot')
            sop.setInput(0, display)
            sop.moveToGoodPosition()
            sop.setDisplayFlag(True)
            if display.isRenderFlagSet():
                sop.setRenderFlag(True)
                sop.parmTuple("p").set(pivot)  
                sop.parm("tx").set(pivot[0]*-1)  
                sop.parm("ty").set(pivot[1]*-1)  
                sop.parm("tz").set(pivot[2]*-1)  
            n.parmTuple("t").set(pivot)
            n.parm("px").set(0)
            n.parm("py").set(0)
            n.parm("pz").set(0)