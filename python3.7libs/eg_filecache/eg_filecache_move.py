import os
import threading
import hou
import shutil
import re

class filecache:

    def __init__(self):
        self.src = None
        self.node = None

    def move_cache(self, kwargs):

        self.node = kwargs['node']

        self.src = kwargs['node'].parm('file').evalAsString()

        # Get Source Filename without Frame only - we need this to copy the correct sequence
        self.source_filename = self.src[self.src.rfind('/') + 1:]
        unex = kwargs['node'].parm('file').unexpandedString()

        r = re.compile(r'[.][$][F][\d]+[.]')

        pos = None
        for m in r.finditer(unex):
            pos = m.start()
        if pos:
            num = m.group()
            r = re.compile(r'\d+')
            for n in r.finditer(num):
                num = int(n.group())

            unex = unex[pos:]

            trim = len(unex) - num
            self.source_filename = self.source_filename[:-trim - num]
        else:
            self.source_filename = self.src[self.src.rfind('/') + 1:]

        trim = self.src.rfind('/')
        self.src = self.src[:trim + 1]

        # Get Source
        try:
            drive, folder_path = os.path.splitdrive(self.src)
        except:
            hou.ui.displayMessage('Source not found. Aborted.')
            return

        if kwargs['node'].parm('file').unexpandedString().startswith('$'):  # has env in beginning
            trim = folder_path[1:].find('/')
            folder_path = folder_path[trim + 1:]

        # Destination
        labels = kwargs['node'].parm('target').menuLabels()
        self.dest = labels[kwargs['node'].parm('target').evalAsInt()]
        self.dest = self.dest[1:]

        self.dest = hou.getenv(self.dest) + folder_path

        if self.src == self.dest:
            hou.ui.displayMessage("Source and Destination are the same. Aborted.")
            return

        # Open Thread so Houdini is not Blocked while copying files
        thread = threading.Thread(target=self.copyfiles, args=())
        thread.start()

    def copyfiles(self):

        # Prepare
        try:
            files = os.listdir(self.src)
        except:
            hou.ui.displayMessage('Source Files not found. Aborted.')
            return

        if not os.path.exists(self.dest):
            try:
                os.makedirs(self.dest)
            except:
                hou.ui.displayMessage('Destination Creation Failed. Copy Aborted')
                return

        hou.ui.displayMessage("Copying for Node " + self.node.path() + " started.")
        for f in files:

            if f.startswith(self.source_filename):
                source = self.src + f
                destination = self.dest + f

                try:
                    if os.path.exists(destination) and self.node.parm('overwrite').evalAsInt():
                        os.remove(destination)
                    shutil.copy2(source, destination)
                    shutil.copystat(source, destination)
                except:
                    print('Copying for file ' + f + ' failed. Continue copying.')

        hou.ui.displayMessage("Copying for Node " + self.node.path() + " finished.")

        # Remove Source
        if self.node.parm('remove_source').eval() == 1:
            try:
                files = os.listdir(self.src)
            except:
                hou.ui.displayMessage('Remove Failed. File does not exist.')
                return

            if len(files) == 0:
                hou.ui.displayMessage('No Source Files found. Removal aborted.')
                return
            for f in files:
                f = self.src + f
                try:
                    os.remove(f)
                except:
                    hou.ui.displayMessage('Remove Failed.')
                    return
            hou.ui.displayMessage("Old Files for Node " + self.node.path() + " removed.")

        # Update Path
        if self.node.parm('update_path').eval() == 1:
            path = self.node.parm('file').unexpandedString()
            path = '$CACHE' + path.strip('$TEMPCACHE')
            self.node.parm('file').set(path)
        return
