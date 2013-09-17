================================================================================
Examples
================================================================================

This page contains several examples of how to use jsonconf.

---------------------------------
Parsing command line arguments
---------------------------------

Here is an example of parsing command line arguments::

    from jsonconf import CommandLineParser


    if __name__ == '__main__':
        parser = CommandLineParser()
        parser.parse()

        print "Program: %s" % parser.getProgram()
        print

        print "Keyword arguments:"
        for key, value in parser.getKeywordArguments().iteritems():
            print "    [%s]: %s" % (key, value)
        print

        print "Extra arguments:"
        for arg in parser.getExtraArguments():
            print "    %s" % arg

Which has the following output::

    $ python basicExample.py
    Program: basicExample.py

    Keyword arguments:

    Extra arguments:


    # python basicExample.py arg1 arg2 key1=123
    Program: basicExample.py

    Keyword arguments:
        [key1]: 123

    Extra arguments:
        arg1
        arg2


    # python basicExample.py hello=world 1=2 verbose flag special1234
    Program: basicExample.py

    Keyword arguments:
        [1]: 2
        [hello]: world

    Extra arguments:
        verbose
        flag
        special12345


Here is an example of specifying command line arguments::

    from jsonconf import CommandLineParser


    def getVerbose(value):
        return value.lower() == "true"


    if __name__ == '__main__':
        parser = CommandLineParser()
        parser.convertKey("name", str)
        parser.convertKey("port", int)
        parser.requireKey("verbose", getVerbose)

        parser.parse()

        name = parser.get("name")
        port = parser.get("port", -1)
        verbose = parser.get("verbose")

        print "name: %s, %s" % (type(name), name)
        print "port: %s, %s" % (type(port), port)
        print "verbose: %s, %s" % (type(verbose), verbose)


Which has the following behavior::

    $ python required.py
    Traceback (most recent call last):
      File "required.py", line 14, in <module>
        parser.parse()
      File "/usr/local/lib/python2.6/dist-packages/jsonconf-0.0.1-py2.6.egg/jsonconf/commandLine.py", line 142, in parse
        raise Exception("Missing required key: %s" % key)
    Exception: Missing required key: verbose

    $ python required.py verbose=123
    name: <type 'NoneType'>, None
    port: <type 'int'>, -1
    verbose: <type 'bool'>, False

    $ python required.py verbose=true name=example port=100
    name: <type 'str'>, example
    port: <type 'int'>, 100
    verbose: <type 'bool'>, True


Several command line variables can also be grouped, or renamed as such::

    from jsonconf import CommandLineParser


    if __name__ == '__main__':
        parser = CommandLineParser()
        parser.renameKeys("verbose", ["-v", "--verbose", "verbose"])
        print parser.getExtraArguments()

Which has the following behavior::

    $ python testRename.py
    []

    $ python testRename.py --verbose
    ["verbose"]

    $ python testRename.py -v
    ["verbose"]

    $ python testRename.py verbose
    ["verbose"]

    $ python testRename.py --verbose -v verbose
    ["verbose"]

This provides the ability to add aliases for a specific piece of functionality
so that it can be configured via many different command line arguments. This is
most useful in grouping single dash and double dash flags (e.g., -v and --verbose).


---------------------------------
Parsing configuration files
---------------------------------

Here is an example of loading a JSON configuration file::

    from jsonconf import ConfigFile


    '''
    Contents of file:

        {
            "verbose": false,
            "logLevel": 100,
            "logFile": "/tmp/myProgram.log"
        }
    '''

    if __name__ == '__main__':
        config = ConfigFile()
        config.parse(filename)

        verbose = config.get("verbose")
        logLevel = config.get("logLevel")
        logFile = config.get("logFile")

        print "verbose: %s, %s" % (type(verbose), verbose)
        print "logLevel: %s, %s" % (type(logLevel), logLevel)
        print "logFile: %s, %s" % (type(logFile), logFile)


This script prints the following::

     $ python testConfig.py
     verbose: <type 'bool'>, False
     logLevel: <type 'int'>, 100
     logFile: <type 'unicode'>, /tmp/myProgram.log


Here is an example with complex data::

    from jsonconf import ConfigFile


    '''
    Contents of file:

        {
            "general": {
                "logging": {
                    "level": 100,
                    "file": "/tmp/program.log"
                }
            },
            "networking": {
                "host": "127.0.0.1",
                "port": 100
            }
        }
    '''


    if __name__ == '__main__':
        config = ConfigFile()
        config.parse(filename)

        logLevel = config.get("general.logging.level")
        logFile = config.get("general.logging.file")
        host = config.get("networking.host")
        port = config.get("networking.port")

        print "Logging: %s, %s" % (logLevel, logFile)
        print "Networking: %s:%s" % (host, port)


Which has the following output::

      $ python complexTest.py 
      Logging: 100, /tmp/program.log
      Networking: 127.0.0.1:100


---------------------------------
Putting it all together
---------------------------------

The following demonstrates the basic usage a JsonConfig::

    from jsonconf import JsonConfig


    '''
    Contents of the file:

        {
            "general": {
                "logging": {
                    "level": 100,
                    "file": "/tmp/program.log"
                }
            },
            "networking": {
                "host": "127.0.0.1",
                "port": 100
            }
        }
    '''

    if __name__ == '__main__':
        config = JsonConfig()
        config.parse(filename)

        logLevel = config.get("general.logging.level")
        logFile = config.get("general.logging.file")
        host = config.get("networking.host")
        port = config.get("networking.port")

        print "Logging: %s, %s" % (logLevel, logFile)
        print "Networking: %s:%s" % (host, port)


Which has the following behavior::

      $ python basicJson.py
      Logging: 100, /tmp/program.log
      Networking: 127.0.0.1:100

      $ python basicJson.py general.logging.level=0 networking.host=localhost
      Logging: 0, /tmp/program.log
      Networking: localhost:100

The JsonConfig class provides the ability to specify command line arguments to
override the configuration options present in a JSON configuration file.

The JSON configuration file can also be specified from the command line
arguments in any of the following ways::

    $ python config.py --config-file=/tmp/config.json
    $ python config.py -c=/tmp/config.json

This command line argument overrides the filename passed to
the :func:`jsonconf.JsonConfig.parse` function.

For further information, please see the documentation on the specific classes.
