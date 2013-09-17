================================================================================
Introduction
================================================================================

The jsonconf module provides the ability to easily configure programs using
a JSON configuration file, and command line arguments.

The JSON configuration file is used to specify a hierarchy of configuration
base options, and the command line can be used to override specific values
on the fly.

For instance, consider the following JSON configuration file::

    {
        "general": {
            "logging": {
                "debugLevel": 0
            }
        }
    }

A Python program can then load this configuration as so::

    from jsonconf import JsonConfig


    if __name__ == '__main__':
       config = JsonConfig()
       config.renameCommandLineArguments("verbose", ["-v", "--verbose"])

       config.parse(filename)


Now, the :class:`jsonconf.JsonConfig` object can be used to access the
configuration options::

    debugLevel = config.get("general.logging.debugLevel")
    verbose = config.hasCommandLineArgument("verbose")

The period is used to reference a sub-key within a JSON object which allows quick
and easy access to keys within a complex JSON object.

The command line can be used to quickly override configuration options
as such::

    $ python test.py general.logging.debugLevel=100 --verbose

This will set the debugLevel key to a value of 100, and set the local
verbose variable to be True.
