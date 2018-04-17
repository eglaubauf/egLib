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
            pivot = geo.boundingBox().center()
            sop = n.createNode('xform', 'move_to_pivot1')
            sop.setInput(0, display)
            sop.moveToGoodPosition()
            sop.setDisplayFlag(True)
            if display.isRenderFlagSet():
                sop.setRenderFlag(True)
                sop.parmTuple("t").set(-pivot)
                sop.parmTuple("p").set( pivot)    
            n.parmTuple("t").set(pivot)



