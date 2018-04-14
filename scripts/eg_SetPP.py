import hou



def run():

    sel = hou.selectedNodes()


    for n in sel:
        if n.type().name() == "geo":
            for c in n.children():
                if c.type().name() == "file":
                    if c.parm("loadtype").evalAsString() != "delayed":
                        c.parm("loadtype").set("delayed")
                        c.parm("packedviewedit").set("box")
                    else:
                        c.parm("loadtype").set("full")
                        c.parm("packedviewedit").set("unchanged")

