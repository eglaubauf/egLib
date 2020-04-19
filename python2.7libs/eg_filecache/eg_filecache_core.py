import hou
import re

class filecache:

    def __init__(self):

        self.node = ''
        self.full_path = ''
        self.full_path_unexpanded = ''
        self.version = ''
        self.expanded = False
        self.parms = {
            'dir': '',
            'folder': '',
            'sub': '',
            'filename': '',
            'suffix': ''
        }

        self.options = ['P_DATE', 'P_NAME', 'P_USER', 'P_VERSION', 'os', 'c_version', 'frames']

    def update_path(self, kwargs):

        self.node = kwargs['node']
        self.expanded = bool(self.node.parm('expanded').evalAsInt())

        for p in self.parms:
            if not self.get_path_options(p):
                return
        self.create_full_path()

        self.update_file_parm()

    def get_global_version(self, kwargs):

        self.node = kwargs['node']

        if kwargs['parm'].evalAsInt():
            path = self.node.parm('file').unexpandedString()
            c_version = hou.getenv('C_VERSION')

            # Find and Replace Version
            r = re.compile(r'[v][\d]')
            pos = None
            pre = ""
            post = ""

            for m in r.finditer(path):
                pos = m.start()

                pre = path[:pos + 1]
                post = path[pos + 4:]

            path = pre + '$C_VERSION' + post
            self.node.parm('file').set(path)

        else:
            self.update_version(kwargs)


    def update_version(self, kwargs):

        self.node = kwargs['node']
        path = self.node.parm('file').unexpandedString()
        self.version = self.node.parm("c_version_val").evalAsInt()

        # Find and Replace Version
        r = re.compile(r'[v][\d]')
        pos = None
        pre = ""
        post = ""

        for m in r.finditer(path):
            pos = m.start()

            pre = path[:pos + 1]
            post = path[pos + 4:]
        # Check for C_VERSION
        if pos == None:
            # Find and Replace Version
            r = re.compile(r'[v][$][C]')
            pos = None
            pre = ""
            post = ""

            for m in r.finditer(path):
                pos = m.start()

                pre = path[:pos + 1]
                post = path[pos + 11:]

        path = pre + str(self.version).rjust(3, '0') + post
        self.node.parm('file').set(path)

    def get_path_options(self, key):
        labels = self.node.parm(key).menuLabels()

        if key == 'dir':
            if labels[self.node.parm(key).evalAsInt()] == 'Custom':
                self.parms[key] = self.node.parm('dir_string').evalAsString()
                return True
        if key == 'folder':
            if labels[self.node.parm(key).evalAsInt()] == 'P_NAME':
                if self.node.parm('fullproj').evalAsInt() == 1:
                    self.parms[key] = '$P_DATE' + '.' + '$P_NAME' + '.' + '$P_USER' + '.' + '$P_VERSION'
                    return True
            if labels[self.node.parm(key).evalAsInt()] == 'Custom':
                self.parms[key] = self.node.parm('folder_string').evalAsString()
                return True
        if key == 'sub':
            if labels[self.node.parm(key).evalAsInt()] == 'Node':
                self.parms[key] = '$OS'
            elif labels[self.node.parm(key).evalAsInt()] == 'Parent':
                self.parms[key] = self.node.parent().name()
            elif labels[self.node.parm(key).evalAsInt()] == 'Custom':
                self.parms[key] = self.node.parm('sub_string').evalAsString()
            return True
        if key == 'filename':
            if labels[self.node.parm(key).evalAsInt()] == 'from Options':
                self.parms[key] = self.build_filename()
            elif labels[self.node.parm(key).evalAsInt()] == 'Custom':
                self.parms[key] = self.node.parm('filename_string').evalAsString()
                if self.node.parm('c_version').evalAsInt():
                    self.version = self.node.parm('c_version_val').evalAsString().rjust(3, '0')
                    self.parms[key] += '.v' + self.version
            return True
        if key == 'suffix':
            if labels[self.node.parm(key).evalAsInt()] == 'Custom':
                self.parms[key] = self.node.parm('suffix_string').evalAsString()
            else:
                self.parms[key] = labels[self.node.parm(key).evalAsInt()]
            return True

        # Get Env Variable if none of above options is set
        user_choice = labels[self.node.parm(key).evalAsInt()]
        env = hou.getenv(user_choice)

        if env:
            self.parms[key] = '$' + user_choice
            return True
        else:
            hou.ui.displayMessage('Variable does not exists - Please lay down an egProject Node first')
            return False

    def build_filename(self):
        filename = ''
        for o in self.options:
            if self.node.parm(o.lower()).evalAsInt():
                if o == 'os':
                    filename += '$OS' + '.'
                elif o == 'frames':
                    filename += '$F4' + '.'
                elif o == 'c_version':
                    self.version = self.node.parm('c_version_val').evalAsString().rjust(3, '0')
                    filename += 'v' + self.version + '.'
                else:
                    env = hou.getenv(o)
                    if env:
                        filename += '$' + o + '.'
                    else:
                        filename += hou.getenv(o) + '.'
        filename = filename[:-1]
        return filename

    def update_file_parm(self):
        # self.full_path_unexpanded = self.full_path

        if self.expanded:
            self.node.parm('file').set(self.full_path)
            self.node.parm('file').set(self.node.parm('file').evalAsString())
        else:
            self.node.parm('file').set(self.full_path)

    def debug_list(self):
        for p in self.parms:
            print(p + ':' + self.parms[p])

    def create_full_path(self):

        if self.node.parm('c_version_folder').evalAsInt():
            self.full_path = self.parms['dir'] + '/' + self.parms['folder'] + '/' + self.parms['sub'] + '/' + self.version + '/' + self.parms['filename'] + self.parms['suffix']
            return
        self.full_path = self.parms['dir'] + '/' + self.parms['folder'] + '/' + self.parms['sub'] + '/' + self.parms['filename'] + self.parms['suffix']

    def show_expanded(self, kwargs):
        if kwargs['parm'].evalAsInt():
            self.expanded = True
            self.update_version_from_string(kwargs)
        else:
            self.expanded = False

    def update_version_from_string(self, kwargs):

        filestring = kwargs['node'].parm('file').evalAsString()

        r = re.compile(r'[.][v][\d]+[.]')

        pos = None
        for m in r.finditer(filestring):
            pos = m.start()
        if pos:
            num = m.group()
            r = re.compile(r'\d+')
            for n in r.finditer(num):
                num = int(n.group())

            kwargs['node'].parm('c_version_val').set(num)
            self.version = num
