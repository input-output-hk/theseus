import Theseus
import unittest2
import json


# This test requires the following data to live in ~/.theseus.secrets
#
# {
#  "strings": "Value",
#  "morestrings": "Value2",
#  "1": "2",
#  "numbers1": 1,
#  "numbers2": 3283923823928371398721389,
#  "numbers3": -50,
#  "subtree": {
#    "subkey": "subvalue"
#  }
# }
#

class TheseusSecrets(unittest2.TestCase):
    @classmethod
    def setupClass(cls):
        cls.secrets = Theseus.Secrets()

    def test_01_strings(self):
        self.assertEqual(self.secrets.get('strings'), 'Value', msg="Correct value returned for strings")
        self.assertEqual(self.secrets.get('morestrings'), 'Value2', msg="Correct value returned for morestrings")
        self.assertEqual(self.secrets.get('1'), '2', msg="Correct value returned for numeric string 1")

    def test_02_numbers(self):
        self.assertEqual(self.secrets.get('numbers1'), 1, msg="Correct numeric value returned")
        self.assertEqual(self.secrets.get('numbers2'), 3283923823928371398721389, msg="Correct value returned for numeric string Key")
        self.assertEqual(self.secrets.get('numbers3'), -50, msg="Correct value returned for negative number")

    def test_03_tree(self):
        self.assertEqual(self.secrets.get('subtree'), json.loads('{"subkey": "subvalue"}'), msg="tree returned")
        self.assertEqual(self.secrets.get('subtree')["subkey"], "subvalue", msg="direct reference to key")


# start unittest2 to run these tests
if __name__ == "__main__":
    unittest2.main()
