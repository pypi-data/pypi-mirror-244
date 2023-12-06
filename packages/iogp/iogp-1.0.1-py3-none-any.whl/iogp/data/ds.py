"""
iogp.data.ds: Data structures.

Author: Vlad  Topan (vtopan/gmail)
"""
import ast
import copy
import os
import pprint
import re


class AttrDict(dict):
    """
    Keys-as-attributes dictionary. Can be used for storing configuration data.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def save(self, filename, skip_keys=None):
        """
        Save the contents to a file (assuming the instance only contains basic types).

        :param skip_keys: Skip these (top-level) keys when saving (list/tuple).
        """
        data = self
        if skip_keys:
            data = copy.deepcopy(data)
            for k in skip_keys:
                data.pop(k)
        open(filename, 'w', encoding='utf8').write(pprint.pformat(data))

    def load(self, filename, errors='replace'):
        """
        Load the dict from a file (converting top-level dicts to AttrDict).
        """
        if not os.path.isfile(filename):
            raise OSError(f'File {filename} not found!')
        try:
            data = open(filename, encoding='utf8', errors=errors).read()
            if not data.strip():
                # empty file
                return
            data = ast.literal_eval(data)
        except Exception as e:
            raise ValueError(f'Failed parsing file: {e}!') from e
        dict_to_AttrDict(data, self)

    def eval_path(self, path, path_key='path'):
        """
        Interpolate a path using the values in self[path_key].
        """
        path = re.sub(r'\$(\w+)', lambda m: self[path_key].get(m.groups()[0], m.groups()[0]), path)
        return os.path.normpath(path)

    def from_dict(self, d):
        """
        Populate from a dict (returning self).
        """
        dict_to_AttrDict(d, self)
        return self



class Config(AttrDict):
    """
    File-based AttrDict for use as a configuration file.
    """

    def __init__(self, filename, template=None):
        if template:
            self.update(copy.deepcopy(template))
        self._filename = filename

    def load(self):
        super().load(self._filename)

    def save(self):
        super().load(self._filename)

    def resolve_cfg_paths(self, paths=None):
        """
        Resolve an AttrDict containing inter-referencing paths and normalize (\ -> /)

        Sample input: `AttrDict(root='/path', subpath='<root>/custompath')`
        """
        paths = paths or self['path']
        for k, v in paths.items():
            paths[k] = paths[k].replace('\\', '/')
        any = 1
        while any:
            any = 0
            for k, v in paths.items():
                if m := re.search(r'\$(\w+)', v):
                    any = 1
                    pattern, name = m.group(0, 1)
                    if name not in paths:
                        raise ValueError(f'Invalid path key referenced "{name}" by "{k}"!')
                    paths[k] = v.replace(pattern, paths[name])



def dict_to_AttrDict(source, dest=None):
    """
    Recursively convert a dict to an AttrDict.
    """
    res = AttrDict() if dest is None else dest
    for k, v in source.items():
        if type(v) is dict:
            v = dict_to_AttrDict(v)
        res[k] = v
    return res
