import hou



def run():

    sel = hou.selectedNodes()

    #Create Dialog
    selected = hou.ui.displayMessage('Do you want to set to Packed Prims or Full Load?', buttons=('Set to Packed','Set To Full-Load', 'Abort'), default_choice=0, close_choice=2)

    for n in sel:
        if n.type().name() == "geo":
            for c in n.children():
                if c.type().name() == "file":
                    if selected == 0:
                        c.parm("loadtype").set("delayed")
                        #c.parm("packedviewedit").set("box")
                        c.parm("viewportlod").set("full")
                    elif selected == 1:
                        c.parm("loadtype").set("full")
                        c.parm("packedviewedit").set("unchanged")

