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
        raise NotImplementedError

    @staticmethod
    def create(path):
        raise NotImplementedError        

    def __init__(self, path):
        #self.assets
        raise NotImplementedError

    def sync(self, asset):
        raise NotImplementedError

    def create_asset(self, asset):
        raise NotImplementedError

    def delete_asset(self, asset):
        raise NotImplementedError        


class Asset(object):
    def __init__(self, path):
        #self.name
        #self.entities
        raise NotImplementedError

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
        #self.name
        #self.path
        raise NotImplementedError

    def open(self):
        raise NotImplementedError

    def reference(self):
        raise NotImplementedError

    def browse(self):
        raise NotImplementedError

    def get_log(self):
        raise NotImplementedError

    def switch_ver(self, commit):
        raise NotImplementedError
