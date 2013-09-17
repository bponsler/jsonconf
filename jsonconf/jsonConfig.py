from configFile import ConfigFile
from commandLine import CommandLineParser


class JsonConfig:
    '''The JsonConfig class provides the ability to configure
    a project using a JSON configuration file as well as command line
    arguments.

    This class manages parsing the JSON configuration file into a dictionary
    configuration options, and also manages parsing the command line arguments.

    This class allows command line arguments to be specified in order to
    dynamically override specific configuration options.

    For example, given the following JSON configuration file::

        {
            "one": 1,
            "var1": {
                "var2": "hello"
            }
        }
    
    And the following command line arguments::

        /usr/bin/program one=5 var1.var2=goodbye

    The following is true::

        jsonConf.get("one") == "5"
        jsonConf.get("var1.var2") == "goodbye"

    This class also provides an interface for converting specified key
    value pairs into a desired type using a conversion function, as well
    as requiring specific key value pairs to exist.

    The JsonConfig class accepts the following command line arguments
    which can be used to specify the JSON configuration file to use from
    the command line::

        --config-file=/tmp/config.json
        -c=/tmp/config.json

    This command line argument overrides the filename passed to the
    :func:`jsonconf.JsonConfig.parse` function.

    '''
    __ConfigFileKey = "configFile"

    def __init__(self):
        '''Create a JsonConfig object.'''
        self.__configFile = ConfigFile()
        self.__commandLine = CommandLineParser()

        self.__requiredKeys = []
        self.__keyConverters = {}

        # Allow the specification of the JSON configuration file via the
        # command line
        self.__commandLine.renameKeys(self.__ConfigFileKey,
                                      ["-c", "--config-file"])

    def parse(self, filename=None, args=None):
        '''Parse the given JSON configuration file, and the command
        line arguments.

        :param filename: The path to the JSON configuration file
        :param args: The list of command line arguments

        '''
        # Parse the command line arguments first, in case the configuration
        # file is specified
        self.__commandLine.parse(args)

        # Use the filename specified on the command line, if one exists,
        # otherwise use the argument to this function
        filename = self.__commandLine.get(self.__ConfigFileKey, filename)

        # Parse the desired configuration file
        self.__configFile.parse(filename)

        # Command line arguments override the configuration file
        clData = self.__commandLine.getKeywordArguments()
        self.__configFile.updateData(clData)

        # Ensure all required keys are specified, and attempt to convert
        # all keys to their specified types
        self.__configFile.requireKeys(self.__requiredKeys)
        self.__configFile.convertKeys(self.__keyConverters)

    def convertKey(self, key, converterFn):
        '''Specify a conversion function to be applied to the given key
        value pair.

        `converterFn` must have the following signature::

            converterFn(value)

        :param key: The key
        :param converterFn: The conversion function

        '''
        if converterFn is not None:
            self.__keyConverters[key] = converterFn

    def requireKey(self, key, converterFn=None):
        '''Require the given key value pair to be specified by either
        the command line or the JSON configuration file.

        `converterFn` must have the following signature::

            converterFn(value)

        :param key: The key
        :param converterFn: The conversion function

        '''
        self.__requiredKeys.append(key)
        self.convertKey(key, converterFn)

    def renameCommandLineArguments(self, newKey, keys):
        '''Rename any command line arguments in the given list to
        the given new key name.

        :param newKey: The key to which the keys will be renamed
        :param keys: The list of keys to rename

        '''
        self.__commandLine.renameKeys(newKey, keys)

    def hasKey(self, key):
        '''Determine if the given configuration key is specified.

        :param key: The key
        :rtype: bool

        '''
        return self.__configFile.hasKey(key)

    def get(self, key, default=None):
        '''Get the value of the given configuration key.

        :param key: The key
        :param default: The default value returned if the key does not exist

        '''
        return self.__configFile.get(key, default)

    def hasCommandLineArgument(self, arg):
        '''Determine if the given command line argument was specified.

        For example, given the following command line arguments::

            /usr/bin/whatever arg1 var1=123 arg2 var2=hello

        The function behaves as follows::

            self.hasCommandLineArgument("arg1") == True
            self.hasCommandLineArgument("arg2") == True
            self.hasCommandLineArgument("var1") == False
            self.hasCommandLineArgument("var2") == False

        This function returns True if the given argument was specified
        as a non-keyword command line argument.

        :param arg: The command line argument
        :rtype: bool

        '''
        return arg in self.__commandLine.getExtraArguments()

    def getCommandLineArguments(self):
        '''Return the list of (non key value pair) command line arguments.

        For example, given the following command line arguments::

            /usr/bin/whatever arg1 var1=123 arg2 var2=hello

        This functions returns::

            ["arg1", "arg2"]

        :rtype: List of strings

        '''
        return self.__commandLine.getExtraArguments()
