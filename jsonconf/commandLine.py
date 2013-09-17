import sys
from copy import deepcopy


class CommandLineParser:
    '''The CommandLineParser class encapsulates the logic of parsing
    command line arguments and converting them into a set of key value
    pairs, and a list of non key value pair arguments.

    For example, given the following command line arguments::

        /usr/bin/whatever arg1 var1=type1 arg2 var2=type2 var1.var2.var3=value

    The following dictionary of key value pairs is produced::

        {
            "var1": "type1",
            "var2": "type2",
            "var1.var2.var3": "value"
        }

    And the following list of non key value pairs is produced::

        ["arg1", "arg2"]

    Key value pairs must be a single string separated by an equal sign.
    Non key value pairs are any string that does not contain an equal sign.

    The order for arguments does not matter.

    '''

    def __init__(self):
        '''Create the CommandLineParser object.'''
        self.__program = None
        self.__extraArgs = []
        self.__keyArgs = {}
        self.__requiredKeys = {}
        self.__keyConverters = {}
        self.__renameMap = {}

    def get(self, key, default=None):
        '''Get the value specified for the given key.

        :param key: The key
        :param default: The default value returned if the key was not specified
        :rtype: The value for the specified key

        '''
        return self.__keyArgs.get(key, default)

    def getKeywordArguments(self):
        '''Return the dictionary of keyword arguments.

        :rtype: A dictionary of key value pairs

        '''
        return self.__keyArgs

    def getExtraArguments(self):
        '''Get the list of non keyword arguments.

        :rtype: List of strings

        '''
        return self.__extraArgs

    def getProgram(self):
        '''Get the name of the program.

        :rtype: string

        '''
        return self.__program

    def convertKey(self, key, converterFn):
        '''Specify a conversion function to be used to convert the
        value of a key value pair.

        Conversion functions must have the following signature::

            converterFn(value)

        :param key: The key
        :param converterFn: The conversion function
        
        '''
        if converterFn is not None:
            self.__keyConverters[key] = converterFn

    def requireKey(self, key, converter=None):
        '''Require the given key value pair to be specified.

        Conversion functions must have the following signature::

            conversionFn(value)

        :param key: The key
        :param converter: The optional conversion function

        '''
        self.__requiredKeys[key] = converter
        self.convertKey(key, converter)

    def renameKeys(self, newKey, keys):
        '''Rename the given list of keys to a single key. The new names
        apply to both keyword and non-keyword arguments.

        :param newKey: The key to which the keys will be renamed
        :param keys: The list of keys to rename

        '''
        for key in keys:
            self.__renameMap[key] = newKey

    def parse(self, argv=None):
        '''Parse the given command line arguments. If the list is not
        specified, then it defaults to the system command line arguments
        (i.e., sys.argv).

        :param argv: The list of command line arguments.

        :raises Exception: If one of the required keys is not specified as
                           a key value pair
        :raises Exception: If one of the type conversion functions produces
                           an error during the conversion

        '''
        argv = sys.argv if argv is None else argv

        # Parse arguments into a dictionary of keyword arguments and
        # a list of non-keyword arguments
        self.__parseArgs(argv)

        # Rename all of the specified keys
        self.__keyArgs = self.__renameKeys(self.__keyArgs)
        self.__extraArgs = self.__renameExtraArguments()

        # Ensure all required keys are specified as key value pairs
        for key, converter in self.__requiredKeys.iteritems():
            if key not in self.__keyArgs:
                raise Exception("Missing required key: %s" % key)

        # Attempt to convert all of the types
        for key, converter in self.__keyConverters.iteritems():
            value = self.__keyArgs.get(key, None)
            if value is not None and converter is not None:
                try:
                    # Convert the value using the desired function
                    self.__keyArgs[key] = converter(value)
                except Exception, e:
                    msg = "Failed to convert key [%s]: %s" % (key, e)
                    raise Exception(msg)

    def __getitem__(self, key):
        '''Get the value specified for the given key.

        :param key: The key
        :rtype: The value for the specified key

        '''
        return self.get(key, None)

    ##### Private functions

    def __renameExtraArguments(self):
        '''Rename all of the extra command line arguments.

        :rtype: List of strings which have been renamed

        '''
        extraArgs = []

        # Re-name all keys which need to be re-named
        for key in self.__extraArgs:
            key = self.__renameMap.get(key, key)
            if key not in extraArgs:
                extraArgs.append(key)

        return extraArgs

    def __renameKeys(self, keyArgs):
        '''Rename all specified keys.

        :param keyArgs: The current dictionary of keyword arguments
        :rype: dictionary with renamed keys

        '''
        if type(keyArgs) != type(dict()):
            return keyArgs

        # The dictionary containing renamed values
        result = {}

        # Rename all of the keys in the current object
        for key, value in keyArgs.iteritems():
            # Recurse to rename all sub-keys
            renamedValue = self.__renameKeys(value)

            # Store the value by the renamed key, or the orignal key
            # depending of this key is expected to be renamed
            renamedKey = self.__renameMap.get(key, None)
            if renamedKey is None:
                result[key] = renamedValue
            else:
                result[renamedKey] = renamedValue

        return result

    def __parseArgs(self, argv):
        '''Parse the given list of command line arguments.

        :param argv: The list of command line arguments.

        '''
        if len(argv) > 0:
            self.__program = argv[0]

            # Skip the program name
            for arg in argv[1:]:
                parts = arg.split("=")
                if len(parts) == 2:
                    self.__keyArgs[parts[0]] = parts[1]
                else:
                    self.__extraArgs.append(arg)
