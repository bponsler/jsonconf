from unittest import TestCase

from jsonconf import JsonConfig


class JsonConfigTests(TestCase):
    def setUp(self):
        self.__testFile = "/tmp/testJson.json"

    def test_constructor(self):
        config = JsonConfig()
        self.assertTrue(config is not None)
        config.parse()

    def test_missingFile(self):
        config = JsonConfig()
        self.assertRaises(Exception, config.parse,
                          "/tmp/whatever/does/not/exist.json")

    def test_emptyFile(self):
        lines = []
        self.__writeFile(lines)

        config = JsonConfig()
        self.assertRaises(Exception, config.parse, self.__testFile)

    def test_validFile(self):
        lines = [
            "{",
            "}",
            ]
        self.__writeFile(lines)

        config = JsonConfig()
        config.parse(self.__testFile)

    def test_validFile(self):
        lines = [
            "{",
            '    "one": 5',
            "}",
            ]
        self.__writeFile(lines)

        config = JsonConfig()
        config.parse(self.__testFile)

        self.assertEqual(config.hasKey("one"), True)
        self.assertEqual(config.get("one"), 5)

    def test_overrideKey(self):
        lines = [
            "{",
            '    "one": 5',
            "}",
            ]
        self.__writeFile(lines)

        args = ["/usr/bin/whatever", "one=100"]

        config = JsonConfig()
        config.parse(self.__testFile, args)

        self.assertEqual(config.hasKey("one"), True)
        self.assertEqual(config.get("one"), '100')

    def test_overrideKey2(self):
        lines = [
            "{",
            '    "one": {',
            '        "two": 5',
            '    }',
            "}",
            ]
        self.__writeFile(lines)

        args = ["/usr/bin/whatever", "one.two=100"]

        config = JsonConfig()
        config.parse(self.__testFile, args)

        self.assertEqual(config.hasKey("one"), True)
        self.assertEqual(config.hasKey("one.two"), True)
        self.assertEqual(config.get("one"), {"two": '100'})
        self.assertEqual(config.get("one.two"), '100')

    def test_requireKey(self):
        lines = [
            "{",
            "}",
            ]
        self.__writeFile(lines)

        args = ["/usr/bin/whatever"]

        config = JsonConfig()
        config.requireKey("one")
        self.assertRaises(Exception, config.parse, self.__testFile, args)

    def test_requireKey2(self):
        lines = [
            "{",
            '    "one": "hello"',
            "}",
            ]
        self.__writeFile(lines)

        args = ["/usr/bin/whatever"]

        config = JsonConfig()
        config.requireKey("one")
        # TODO: should require in either file or CL args....
        config.parse(self.__testFile, args)

    def test_requireKey3(self):
        lines = [
            "{",
            '    "one": "hello"',
            "}",
            ]
        self.__writeFile(lines)

        args = ["/usr/bin/whatever"]

        config = JsonConfig()
        config.requireKey("one", int)

        # TODO: should require in either file or CL args....

        # Cannot convert string to int
        self.assertRaises(Exception, config.parse, self.__testFile, args)

    def test_requireKey3(self):
        lines = [
            "{",
            '    "one": 5',
            "}",
            ]
        self.__writeFile(lines)

        args = ["/usr/bin/whatever"]

        config = JsonConfig()
        config.requireKey("one", int)

        # Cannot convert string to int
        config.parse(self.__testFile, args)

    def test_filename(self):
        lines = []
        self.__writeFile(lines)

        args = ["/usr/bin/whatever", "--config-file=/tmp/does/not/exist.json"]

        config = JsonConfig()
        self.assertRaises(Exception, config.parse, args=args)  # Invalid file

        lines = [
            "{",
            '    "logLevel": 123',
            "}"
            ]
        self.__writeFile(lines)

        args = ["/usr/bin/whatever", "--config-file=%s" % self.__testFile]

        config = JsonConfig()
        config.parse(args=args)

        self.assertEqual(config.get("logLevel"), 123)

    def __test_overrideFilename(self):
        args = ["/usr/bin/whatever", "--config-file=%s" % self.__testFile]

        config = JsonConfig()

        # Command line filename overrides the one specified here
        config.parse(filename="/tmp/this/file/does/not/exist", args=args)

        self.assertEqual(config.get("logLevel"), 123)

    ##### Private functions

    def __writeFile(self, lines):
        fd = open(self.__testFile, 'w')
        for line in lines:
            fd.write("%s\n" % line)
        fd.close()
