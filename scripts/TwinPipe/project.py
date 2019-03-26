import os
import os.path
import shutil
import maya_interop as dcc
import os_interop as os_inter
reload(dcc)
reload(os_inter)

ASSET_TYPES = {
    'scene': 'Scenes',
    'env': 'Environments',
    'prop': 'Props',
    'char': 'Characters'
}

ENTITY_TYPES = {
    'scene': ['layout', 'blocking', 'polish', 'lighting'],
    'env': ['blocking', 'rough', 'model'],
    'prop': ['rough', 'model', 'rig'],
    'char': ['rough', 'model', 'rig']
}


def get_template_scene(path):
    # get back to the project root
    while not 'twinpipe.json' in os.listdir(path):
        old = path
        path = os.path.split(path)[0]
        assert(old != path)

    # return template scene
    template = os.path.join(path, 'new_file_template.ma')
    if not os.path.exists(template):
        dcc.new_scene()
        dcc.save_scene(template)
        dcc.new_scene()

    return template

class Project(object):
    @staticmethod
    def load(path):
        if not os.path.exists(path):
            raise ValueError

        # check if is maya workspace and has twinpipe metadata
        contents = os.listdir(path)
        print contents
        if not 'workspace.mel' in contents or not 'twinpipe.json' in contents:
            raise ValueError

        return Project(path)

    @staticmethod
    def create(path):
        raise NotImplementedError

    def __init__(self, path):
        self.path = path
        self.assets = {}

        for atype in ASSET_TYPES.keys():
            base = self._path_for_atype(atype)

            if not os.path.exists(base):
                os.makedirs(base)

            folders = [x for x in [os.path.join(base, y) for y in os.listdir(base)] if os.path.isdir(x)]
            self.assets[atype] = [Asset(x, atype) for x in folders]

    def sync(self, asset):
        raise NotImplementedError

    def create_asset(self, atype, name):
        path = os.path.join(self._path_for_atype(atype), name)
        if os.path.exists(path):
            dcc.error_message("This asset already exists")
            return

        os.makedirs(path)

        self.assets[atype].append(Asset(path, atype))

    def delete_asset(self, asset):
        contents = os.listdir(asset.path)
        if contents:
            assert(0 != len([x for x in contents if x.endswith('.ma') or x.endswith('.mb')]))

        shutil.rmtree(asset.path)
        self.assets[asset.atype].remove(asset)

    def _path_for_atype(self, atype):
        if atype != 'scene':
            base = os.path.join(self.path, 'assets', atype)
        else:
            base = os.path.join(self.path, 'scenes')

        return base

class Asset(object):
    def __init__(self, path, atype):
        self.name = os.path.split(path)[1]
        self.path = path
        self.atype = atype

        maya_files = [os.path.join(path, x) for x in os.listdir(path) if x.endswith('.ma') or x.endswith('.mb')]
        self.entities = [Entity(x) for x in maya_files]

    def create_entity(self, name):
        self.entities.append(Entity.create(self.name, self.atype, name, self.path))

    def delete_entity(self, entity):
        os.remove(entity.path)
        self.entities.remove(entity)

    def promote(self, from_entity, to_entity):
        raise NotImplementedError

    def commit(self, log):
        raise NotImplementedError

class Entity(object):
    @staticmethod
    def create(name, atype, entity_name, path):
        file_name = '_'.join([name, atype, entity_name]) + '.ma'
        file_path = os.path.join(path, file_name)
        shutil.copy(get_template_scene(path), file_path)

        return Entity(file_path)

    def __init__(self, path):
        self.name = os.path.split(path)[1].split('.')[0].split('_')[2]    # FIXME: (this could be bad if there are multiple dots)
        self.path = path

    def open(self):
        dcc.open_scene(self.path)

    def reference(self):
        dcc.reference_scene(self.path)

    def browse(self):
        os_inter.show_path(self.path)

    def get_log(self):
        raise NotImplementedError

    def switch_ver(self, commit):
        raise NotImplementedError
