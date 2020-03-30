import hou
import eg_incrSave
import datetime

class project:

    def __init__(self):
        pass

    def updateEntry(self, kwargs):
        val = kwargs['parm']
        env_var = (kwargs['parm_name'].upper())
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

        list = basename.split('_')

        if len(list) == 4:
            # Set DATE
            kwargs['node'].parm('p_date').set(list[0])
            # Set NAME
            kwargs['node'].parm('p_name').set(list[1])
            # Set USER
            kwargs['node'].parm('p_user').set(list[2])
            # SET VERSION
            kwargs['node'].parm('p_version').set(list[3])
        else:
            kwargs['node'].parm('p_name').set(basename)
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

    def incr_save(self, kwargs):
        iSave = eg_incrSave.incrSave()
        iSave.run()

        version = iSave.getCurrentVersion()
        kwargs['node'].parm('p_version').set(version)
