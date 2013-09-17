from unittest import TestCase

from jsonconf import CommandLineParser


class ConfigTests(TestCase):
    def setUp(self):
        pass

    def test_constructor(self):
        parser = CommandLineParser()
        self.assertTrue(parser is not None)
        self.assertEqual(parser.getKeywordArguments(), {})
        self.assertEqual(parser.getExtraArguments(), [])
        self.assertEqual(parser.getProgram(), None)

    def test_emptyArgs(self):
        args = []
        parser = CommandLineParser()
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), {})
        self.assertEqual(parser.getExtraArguments(), [])
        self.assertEqual(parser.getProgram(), None)

    def test_singleArg(self):
        args = ["/usr/bin/whatever"]
        parser = CommandLineParser()
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), {})
        self.assertEqual(parser.getExtraArguments(), [])
        self.assertEqual(parser.getProgram(), "/usr/bin/whatever")

    def test_extraArgs(self):
        extraArgs = ["one", "two", "-d", "--ignore"]

        args = ["/usr/bin/whatever"]
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), {})
        self.assertEqual(parser.getExtraArguments(), extraArgs)
        self.assertEqual(parser.getProgram(), "/usr/bin/whatever")

    def test_keyArgs(self):
        kwargs = {
            "one": '1',
            "two": "2",
            "-d": "hello",
            "--ignore": '5',
            }
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), kwargs)
        self.assertEqual(parser.getExtraArguments(), extraArgs)
        self.assertEqual(parser.getProgram(), "/usr/bin/whatever")

    def test_complexKey(self):
        kwargs = {
            "one.two.three": '1',
            }
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), kwargs)
        self.assertEqual(parser.getExtraArguments(), extraArgs)
        self.assertEqual(parser.getProgram(), "/usr/bin/whatever")

    def test_both(self):
        kwargs = {
            "one": '1',
            "two.three": '1',
            }
        extraArgs = ["--test", "-v"]

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), kwargs)
        self.assertEqual(parser.getExtraArguments(), extraArgs)
        self.assertEqual(parser.getProgram(), "/usr/bin/whatever")

    def test_requiredTest(self):
        kwargs = {}
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.requireKey("verbose")
        self.assertRaises(Exception, parser.parse, args)

    def test_requiredTest2(self):
        kwargs = {"--verbose": 1}
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.requireKey("--verbose")
        parser.parse(args)

    def test_invalidConverter(self):
        kwargs = {"--verbose": "hello"}
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()

        # Cannot parse string to int
        parser.requireKey("--verbose", int)
        self.assertRaises(Exception, parser.parse, args)

    def test_invalidConverter(self):
        kwargs = {"--verbose": "1"}
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.requireKey("--verbose", int)
        parser.parse(args)

    def test_renameKeywordArguments(self):
        kwargs = {"--verbose": "1"}
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.get("verbose"), "1")
        self.assertEqual(parser.getExtraArguments(), [])


        kwargs = {"-v": "1"}
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.get("verbose"), "1")
        self.assertEqual(parser.getExtraArguments(), [])


        kwargs = {"verbose": "1"}
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.get("verbose"), "1")
        self.assertEqual(parser.getExtraArguments(), [])


        kwargs = {"verb": "1"}
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.get("verbose"), "1")
        self.assertEqual(parser.getExtraArguments(), [])


        kwargs = {"verbose": "1", "--verbose": "1", "-v": "1", "verb": "1"}
        extraArgs = []

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.get("verbose"), "1")
        self.assertEqual(parser.getExtraArguments(), [])

    def test_renameExtraArguments(self):
        kwargs = {}
        extraArgs = ["-v"]

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), {})
        self.assertEqual(parser.getExtraArguments(), ["verbose"])


        extraArgs = ["--verbose"]

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), {})
        self.assertEqual(parser.getExtraArguments(), ["verbose"])


        extraArgs = ["verbose"]

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), {})
        self.assertEqual(parser.getExtraArguments(), ["verbose"])


        extraArgs = ["verb"]

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), {})
        self.assertEqual(parser.getExtraArguments(), ["verbose"])


        extraArgs = ["-v", "--verbose", "verb", "verbose"]

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), {})
        self.assertEqual(parser.getExtraArguments(), ["verbose"])


    def test_renameOtherArgs(self):
        kwargs = {"test": "255"}
        extraArgs = ["--verbose", "otherArg"]

        args = ["/usr/bin/whatever"]
        args.extend(map(lambda i: "%s=%s" % (i[0], i[1]), kwargs.items()))
        args.extend(extraArgs)

        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose", "verb"])
        parser.parse(args)

        self.assertEqual(parser.getKeywordArguments(), {"test": "255"})
        self.assertEqual(parser.getExtraArguments(), ["verbose", "otherArg"])
