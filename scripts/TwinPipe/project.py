import os
import os.path
import maya_interop as dcc
reload(dcc)

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

class Project(object):
    @staticmethod
    def load(path):
        if not os.path.exists(path):
            raise ValueError

        # check if is maya workspace and has twinpipe metadata
        contents = os.listdir(path)
        if not 'workspace.mel' in contents or not 'twinpipe.json' in contents:
            return ValueError

        return Project(path)

    @staticmethod
    def create(path):
        raise NotImplementedError        

    def __init__(self, path):
        self.path = path
        self.assets = {}

        for atype in ASSET_TYPES.keys():
            if atype != 'scene':
                base = os.path.join(self.path, 'assets', atype)
            else:
                base = os.path.join(self.path, 'scenes')

            if not os.path.exists(base):
                continue

            folders = [x for x in [os.path.join(base, y) for y in os.listdir(base)] if os.path.isdir(x)]
            self.assets[atype] = [Asset(x) for x in folders]

    def sync(self, asset):
        raise NotImplementedError

    def create_asset(self, asset):
        raise NotImplementedError

    def delete_asset(self, asset):
        raise NotImplementedError        


class Asset(object):
    def __init__(self, path):
        self.name = os.path.split(path)[1]
        self.path = path
        
        maya_files = [os.path.join(x) for x in os.listdir(path) if x.endswith('.ma') or x.endswith('.mb')]
        self.entities = [Entity(x) for x in maya_files]

    def create_entity(self, name):
        raise NotImplementedError

    def delete_entity(self, entity):
        raise NotImplementedError

    def promote(self, from_entity, to_entity):
        raise NotImplementedError

    def commit(self, log):
        raise NotImplementedError

class Entity(object):
    def __init__(self, path):
        self.name = os.path.split(path)[1].split('.')[0]    # FIXME: (this could be bad if there are multiple dots)
        self.path = path

    def open(self):
        dcc.open_scene(self.path)

    def reference(self):
        dcc.reference_scene(self.path)

    def browse(self):
        raise NotImplementedError

    def get_log(self):
        raise NotImplementedError

    def switch_ver(self, commit):
        raise NotImplementedError
