import typing
import json
from pathlib import Path
import Theseus


class Secrets:
    def __init__(self):
        self._storage = typing.Dict[str, any]
        self._backing = "{0}/{1}".format(Path.home(), '.theseus.secrets')

        self.logger = Theseus.get_logger('secrets')

        try:
            json_data = open(self._backing).read()
        except Exception as e:
            self.logger.fatal('Error reading secrets file: {0}'.format(e))

        self._storage = json.loads(json_data)

    def get(self, key: str):
        if key in self._storage:
            return self._storage[key]
        else:
            self.logger.fatal('Key:"{0}" not found'.format(key))
            return ''
