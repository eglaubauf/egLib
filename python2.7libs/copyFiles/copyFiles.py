## Code courtesy of User Dmytro on Stackoverflow
# https://stackoverflow.com/questions/22078621/python-how-to-copy-files-fast
# used under CC-BY-SA as required by Stackoverflow
# https://stackoverflow.com/help/licensing

import os
import sys

class copyFiles:

    class CTError(Exception):
        def __init__(self, errors):
            self.errors = errors

    def __init__(self, path, dest):

        self.path = path
        self.dest = dest
        self.init_flags()
        self.copytree(path, dest)

    def init_flags(self):
        try:
            O_BINARY = os.O_BINARY
            self.READ_FLAGS = os.O_RDONLY | O_BINARY
            self.WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | O_BINARY
            self.BUFFER_SIZE = 128*1024
        except:
            O_BINARY = 0
            self.READ_FLAGS = os.O_RDONLY | O_BINARY
            self.WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | O_BINARY
            self.BUFFER_SIZE = 128*1024

    def copy(self):
        self.copytree(self.path, self.dest)

    def copyfile(self, src, dst):
        try:

            fin = os.open(src, self.READ_FLAGS)
            stat = os.fstat(fin)
            fout = os.open(dst, self.WRITE_FLAGS, stat.st_mode)
            for x in iter(lambda: os.read(fin, self.BUFFER_SIZE), ""):
                os.write(fout, x)
        finally:
            try: os.close(fin)
            except: pass
            try: os.close(fout)
            except: pass

    def copytree(self, src, dst, symlinks=False, ignore=[]):
        names = os.listdir(src)

        if not os.path.exists(dst):
            os.makedirs(dst)
        errors = []
        for name in names:
            if name in ignore:
                continue
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            try:
                if symlinks and os.path.islink(srcname):
                    linkto = os.readlink(srcname)
                    os.symlink(linkto, dstname)
                elif os.path.isdir(srcname):
                    self.copytree(srcname, dstname, symlinks, ignore)
                else:
                    self.copyfile(srcname, dstname)
            except (IOError, os.error), why:
                errors.append((srcname, dstname, str(why)))
            except self.CTError, err:
                errors.extend(err.errors)
        if errors:
            raise self.CTError(errors)


if __name__ == '__main__':
    path = sys.argv[1]
    dest = sys.argv[2]

    c = copyFiles(path, dest)
    c.copy()
