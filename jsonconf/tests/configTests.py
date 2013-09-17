from unittest import TestCase

from jsonconf import ConfigFile


class ConfigTests(TestCase):
    def setUp(self):
        self.__testFile = "/tmp/testJson.json"

    def test_constructor(self):
        config = ConfigFile()
        self.assertTrue(config is not None)
        self.assertTrue(config.delimiter() is not None)

        config = ConfigFile(delimiter='-')
        self.assertTrue(config is not None)
        self.assertTrue(config.delimiter() is not None)

    def test_missingFile(self):
        config = ConfigFile()
        self.assertRaises(Exception, config.parse,
                          "/tmp/missing/directory/noFile.json")

    def test_emptyFile(self):
        self.__writeFile([])

        # Invalid JSON
        config = ConfigFile()
        self.assertRaises(ValueError, config.parse, self.__testFile)

    def test_invalidJson(self):
        lines = [
            "{",
            "    invalid:",
            "}",
            ]
        self.__writeFile(lines)

        # Invalid JSON
        config = ConfigFile()
        self.assertRaises(ValueError, config.parse, self.__testFile)

    def test_simpleJson(self):
        lines = [
            "{",
            "}",
            ]
        self.__writeFile(lines)

        config = ConfigFile()
        config.parse(self.__testFile)

        # No data
        self.assertEqual(config.keys(), [])

    def test_invalidKey(self):
        # Config file keys cannot contain the delimiter
        lines = [
            "{",
            '    "a.b": 1234',
            "}",
            ]
        self.__writeFile(lines)

        config = ConfigFile()
        self.assertRaises(Exception, config.parse, self.__testFile)

        lines = [
            "{",
            '    "a": 1234',
            '    "b": {',
            '        "c": {',
            '            "d-e": 5',
            '        }',
            '    }',
            "}",
            ]
        self.__writeFile(lines)

        # Check that sub objects also fail the verification
        config = ConfigFile(delimiter='-')
        self.assertRaises(Exception, config.parse, self.__testFile)

    def test_simpleKey(self):
        lines = [
            "{",
            '    "key": 1234',
            "}",
            ]
        self.__writeFile(lines)

        config = ConfigFile()
        config.parse(self.__testFile)

        # Test keys
        self.assertEqual(config.keys(), ['key'])
        self.assertEqual(config.hasKey('key'), True)
        self.assertEqual(config.get('key'), 1234)

    def test_complexKey(self):
        lines = [
            "{",
            '    "key1": {',
            '        "key2": {',
            '            "key3": false',
            '        }',
            '    }'
            "}",
            ]
        self.__writeFile(lines)

        config = ConfigFile()
        config.parse(self.__testFile)

        # Test keys
        self.assertEqual(config.keys(), ['key1'])  # Only the outter most key
        self.assertEqual(config.hasKey('key1'), True)
        self.assertEqual(config.hasKey('key1.key2'), True)
        self.assertEqual(config.hasKey('key1.key2.key3'), True)
        self.assertEqual(config.get('key1'), {'key2': {'key3': False}})
        self.assertEqual(config.get('key1.key2'), {'key3': False})
        self.assertEqual(config.get('key1.key2.key3'), False)

    def test_complexKey2(self):
        # Same test, different delimiter
        lines = [
            "{",
            '    "key1": {',
            '        "key2": {',
            '            "key3": false',
            '        }',
            '    }'
            "}",
            ]
        self.__writeFile(lines)

        config = ConfigFile(delimiter='>')
        config.parse(self.__testFile)

        # Test keys
        self.assertEqual(config.keys(), ['key1'])  # Only the outter most key
        self.assertEqual(config.hasKey('key1'), True)
        self.assertEqual(config.hasKey('key1>key2'), True)
        self.assertEqual(config.hasKey('key1>key2>key3'), True)
        self.assertEqual(config.get('key1'), {'key2': {'key3': False}})
        self.assertEqual(config.get('key1>key2'), {'key3': False})
        self.assertEqual(config.get('key1>key2>key3'), False)

    def __writeFile(self, lines):
        fd = open(self.__testFile, 'w')
        for line in lines:
            fd.write("%s\n" % line)
        fd.close()
