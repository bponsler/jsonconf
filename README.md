jsonconf
========

jsonconf is a Python module which provides the ability to merge a JSON configuration file and command line arguments into a single set of configuration data which can be used to configure a program.

For full documentation of jsonconf visit [this page](http://bponsler.github.io/jsonconf/index.html).

The latest version is *0.0.1* which was released on 09/17/2013.


## Install and set-up ##

Please see the [documentation](http://bponsler.github.io/jsonconf/index.html) for further details, which includes instructions for installing and configuring jsonconf.

```
$ cd /opt
$ git clone https://github.com/bponsler/jsonconf
$ sudo chown -R $USERNAME:$USERNAME jsonconf

$ cd jsonconf
$ python setup.py build
$ python setup.py install
```


## Basic usage ##

```
from jsonconf import JsonConfig

if __name__ == '__main__':
    config = JsonConfig()
    config.renameKeys("verbose", ["-v", "--verbose"])
    config.require("general.logging.logLevel", int)

    config.parse()

    verbose = config.hasCommandLineArgument("verbose")
    logLevel = config.get("general.logging.logLevel")
```

Please see the [documentation](http://bponsler.github.io/jsonconf/index.html) for more examples.