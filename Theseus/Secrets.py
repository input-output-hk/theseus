import typing
import json
from pathlib import Path
import Theseus


class Secrets:
    """ Secrets - Provides secrets for tests to configure themselves with

    This object will provide access to secrets that can be used to configure tests so that they don't contain configuration details.

    This is important because these tests need to be stored in a public repository so any credentials in them may be abused.

    Currently the secrets data is stored in  ~/.theseus.secrets but this abstracted enough that we could use other
     sources if we need to without changing how tests use this interface.

    Usage:

    With a .theseus.secrets JSON file containing::

        {
          "Daedalus": {
            "user": "ssh_user",
            "host": "IP.AD.DR.ES",
            "port": 8090,
            }
        }

    You can be access the secrets with code as follows::

        from Theseus import Secrets
        self.secrets = Theseus.Secrets()

        you can just give the block directly to the constructor as kwargs , as long as the keys match::

        daedalus = Daedalus(**self.secrets.get('Daedalus'))

        or unpack it a bit more if you want to change the values::

        host = self.secrets.get('Daedalus')['host']
        user = self.secrets.get('Daedalus')['user']
        port = self.secrets.get('Daedalus')['port']

        daedalus = Daedalus(host=host, user=user, port=port)

    You can also fetch the whole key as a Dict and use that , see the get method for more info

    """
    def __init__(self):
        self._storage = typing.Dict[str, any]
        self._backing = "{0}/{1}".format(Path.home(), '.theseus.secrets')

        self.logger = Theseus.get_logger('secrets')
        self.load_secrets()

    def load_secrets(self):
        """ Overwrites current secrets storage with new data """
        json_data = 'error'
        try:
            with open(self._backing) as secrets_file:
                json_data = secrets_file.read()
        except Exception as e:
            self.logger.fatal('Error reading secrets file: {0}'.format(e))

        self._storage = json.loads(json_data)

    def get(self, key: str):
        """ Fetch a secret Value

        Use this to fetch an block from the config file optionally filtering it to a specific key.
        This operation is a fetch from memory so call it as much as you like.

        Args:
               key(str): The name of the key or block to fetch
        Return:

        """
        if key in self._storage:
            return self._storage[key]
        else:
            self.logger.error('Key:"{0}" not found'.format(key))
            return ''
