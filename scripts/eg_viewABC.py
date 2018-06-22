import hou



def run():

    sel = hou.selectedNodes()


    for n in sel:
        if n.type().name() == "geo":
            for c in n.children():
                if c.type().name() == "alembic":
                    if c.parm("viewportlod").evalAsString() != "box":
                        c.parm("viewportlod").set("box")
                        #c.parm("packedviewedit").set("box")
                    else:
                        c.parm("viewportlod").set("full")
                        #c.parm("packedviewedit").set("unchanged")

