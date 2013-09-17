import json
from os.path import exists


class ConfigFile:
    '''The ConfigFile class manages a JSON configuration file. It provides the
    ability to load a configuration file from memory, and access all of the
    configuration key value pairs.

    It provides a notion of keys and subkeys which allows the user to easily
    access data contained with multiple levels of JSON objects. Take the
    following JSON as an example::

        {
            "first": {
                "second": {
                    "third": "hello",
                    "fourth": 123
                }
            }
        }

    The 'third' and 'fourth' entries can be accessed in any of the following
    ways::

        config.get("first")["second"]["third"]  # "hello"
        config.get("first.second")["fourth"]  # 123

        config.get("first.second.third")  # "hello"
        config.get("first.second.fourth")  # 123

    Sub keys can be accessed by separating a set of keys by a delimiter.

    '''

    def __init__(self, delimiter='.'):
        '''
        :param delimiter: The delimiter used to access sub keys

        '''
        self.__delimiter = delimiter
        self.__data = {}

    def delimiter(self):
        '''The delimiter used by this configuration.

        :rtype: string

        '''
        return self.__delimiter

    def parse(self, filename):
        '''Parse the given JSON configuration file.

        :param filename: The path to the JSON configuration file

        '''
        if filename is not None:
            self.__data = self.__parse(filename)
        self.__verifyKeys(self.__data)

    def keys(self):
        '''Return the list of keys specified in this configuration.

        :rtype: list of strings

        '''
        return self.__data.keys()

    def hasKey(self, key):
        '''Determine if the given key is specified in this configuration.

        :param key: The key
        :rtype: bool

        '''
        return self.get(key) is not None

    def get(self, key, default=None):
        '''Get the value specified by the given key.

        :param key: The key
        :param default: The default value to return if the key does not exist

        :returns: The configuration value for the given key

        '''
        keyParts = key.split(self.__delimiter)

        data = self.__data
        for subKey in keyParts:
            if type(data) == type(dict()) and subKey in data:
                data = data.get(subKey)
            else:
                return default

        return data

    def updateData(self, keyValueMap):
        '''Update the current configuration values with the given
        dictionary values.

        :param keyValueMap: Dictionary mapping keys to values

        '''
        # Update all of the data with the given key value pairs
        for key, value in keyValueMap.iteritems():
            self.__setKeyValue(self.__data, key, value)

    def requireKeys(self, requiredKeys):
        '''Require that the given list of keys are specified.

        :param requiredKeys: The list of required keys
        :raises Exception: If one of the required keys is not specified

        '''
        # Ensure all required keys exist
        for key in requiredKeys:
            if not self.hasKey(key):
                raise Exception("Required key was not specified: %s" % key)

    def convertKeys(self, converterMap):
        '''Convert all of keys using conversion functions as specified in the
        given dictionary of key, function pairs.

        Conversion functions must have the following signature::

            conversionFunction(value)

        :param converterMap: A dictionary mapping keys to conversion functions

        :raises Exception: If a conversion function causes an error

        '''
        # Attempt to convert all of the keys
        for key, converter in converterMap.iteritems():
            value = self.get(key, None)
            if converter is not None:
                try:
                    converted = converter(value)
                except Exception, e:
                    msg = "Failed to convert key: %s\n%s" % (key, e)
                    raise Exception(msg)
                else:
                    self.__data[key] = value

    def __getitem__(self, key):
        '''Get the value specified by the given key.

        :param key: The key

        :returns: The configuration value for the given key, or None if
                  the key is not specified

        '''
        return self.get(key)

    ##### Private functions

    def __setKeyValue(self, data, key, value):
        '''Update the given data dictionary with the given key value
        pair in order to convert possibly delimited keys into a
        proper dictionary structure.

        For example, given::

            data = {"a", "b"}
            self.__setKeyValue({"a": "b"}, "one.two.three", 123)
            print data

        The following dictionary is printed::

            {
                "a": "b",
                "one": {
                    "two": {
                        "three": 123
                    }
                }
            }

        :param data: The current data dictionary
        :param key: The current (possibly delimited) key to convert
        :param value: The value for the key

        '''
        index = key.find(".")

        if type(data) != type(dict()):
            raise Exception("Conflicting key entries: %s" % key)

        if index == -1:
            # Final key in the set
            # Allow the key to be overridden
            data[key] = value
        else:
            # More keys remain
            currentKey = key[0:index]
            nextKey = key[index+1:]

            if currentKey not in data:
                data[currentKey] = {}

            newData = data[currentKey]
            self.__setKeyValue(newData, nextKey, value)

    def __verifyKeys(self, data):
        '''Verify that none of the keys in the configuration dictionary
        contain delimiters. The JSON configuration is forced not to use
        delimiters, as it is easier to maintain sub objects.

        :param data: The dictionary of configuration values

        :raises Exception: If one of the configuration keys contains the
                           delimiter character

        '''
        # Only verify dictionary keys
        if type(data) == type(dict()):
            for key, value in data.iteritems():
                if self.__delimiter in key:
                    msg = "Config file keys must not contain the '%s' key. " \
                        "Please use JSON objects instead." % self.__delimiter
                    raise Exception(msg)

    def __parse(self, filename):
        '''Parse a JSON configuration file.

        :param filename: The path to the JSON configuration file
        :rtype: A dictionary

        :raises Exception: If the file does not exist
        :raises ValueError: If the file contains invalid JSON

        '''
        if not exists(filename):
            raise Exception("Could not find file: %s" % filename)

        fd = open(filename, 'r')
        data = json.load(fd)
        fd.close()

        return data
