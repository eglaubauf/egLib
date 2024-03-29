import hou
import eg_save
import datetime
import os

#reload(eg_save)

class project:

    def __init__(self):
        pass

    def updateEntry(self, kwargs):
        val = kwargs['parm']
        env_var = (kwargs['parm_name'].upper())

        if kwargs['parm'].name() == 'c_version':
            val = val.evalAsString().rjust(3, '0')
            hou.putenv(env_var, val)
            return
        hou.putenv(env_var, val.evalAsString())

    def create(self, kwargs):

        self.readFromFile(kwargs)

        # Set Directories
        self.set_job(kwargs)

        cache = hou.getenv('CACHE')
        kwargs['node'].parm('cache').set(cache)

        temp_cache = hou.getenv('TEMPCACHE')
        kwargs['node'].parm('tempcache').set(temp_cache)

        render = hou.getenv('RENDER')
        kwargs['node'].parm('render').set(render)

        temp_render = hou.getenv('TEMPRENDER')
        kwargs['node'].parm('temprender').set(temp_render)

    def readFromFile(self, kwargs):
        path = hou.hipFile.path()
        basename = len(hou.hipFile.basename())
        path = path[:-basename]

        # Set $NAME
        basename = hou.hipFile.basename()
        basename = basename[:basename.rfind(".")]

        base_list = basename.split('_')

        if len(base_list) == 4:
            # Set DATE
            kwargs['node'].parm('p_date').set(base_list[0])
            # Set NAME
            kwargs['node'].parm('p_name').set(base_list[1])
            # Set USER
            kwargs['node'].parm('p_user').set(base_list[2])
            # SET VERSION
            kwargs['node'].parm('p_version').set(base_list[3])
        else:
            # Check against Filename without Seperator
            if len(basename.split('_')) > 1:
                p_name = basename.split('_')[1]
            else:
                p_name = ""
            kwargs['node'].parm('p_name').set(p_name)
            kwargs['node'].parm('p_user').set(hou.getenv('USER'))
            date = str(datetime.date.today()).replace('-','')[2:]
            kwargs['node'].parm('p_date').set(date)
            kwargs['node'].parm('p_version').set('001')

        # Update Env-Vars
        hou.putenv('P_NAME', kwargs['node'].parm('p_name').evalAsString())
        hou.putenv('P_USER', kwargs['node'].parm('p_user').evalAsString())
        hou.putenv('P_DATE', kwargs['node'].parm('p_date').evalAsString())
        hou.putenv('P_VERSION', kwargs['node'].parm('p_version').evalAsString())

    def set_job(self, kwargs):

        path = hou.hipFile.path()
        basename = len(hou.hipFile.basename())
        path = path[:-basename]

        hou.putenv('JOB', path)
        kwargs['node'].parm('job').set(path)

    def save(self, kwargs):

        s = eg_save.Save(kwargs['node'].parm('p_version'))
        path = s.get_path()

        filename = ''
        envs = ['P_DATE', 'P_NAME', 'P_USER', 'P_VERSION']

        for env in envs:
            if hou.getenv(env):
                filename += hou.getenv(env) + '_'

        filename = filename[:-1] + s.getLicenseType()
        s.save(path + filename)

    def incr_save(self, kwargs):
        iSave = eg_save.Save()
        iSave.incrSave()

        version = iSave.getCurrentVersion()
        kwargs['node'].parm('p_version').set(version)
