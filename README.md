# Csound Package Manager - Plugin Repository

This is a repository for csound plugins to be used in coordination
with [cspm], the csound package 
manager.

# Installing plugins

In order to install and manage the plugins define here, use the utility `cspm`. To
install `cspm` do either

```bash
pip3 install cspm
```

or install it via `git`

```bash
git clone https://github.com/csound-plugins/cspm
cd cspm
python3 setup.py install
```

Then you can use it directly:

```bash
cspm list          # list all available plugins
cspm install poly  # install/update the poly plugin
```

## Storage vs Development

This repository is **ONLY** for storage of binaries, not for source code. In the future
this storage will be extended to *user-defined-opcodes* developed in the *csound* language
itself, which will also be installable via `cspm`

-------

# Contributing

In order to add a plugin or a collection of plugins to this repository, fork
this repository and create a PR. 

## Anatomy of a plugin declaration

First you need to add your plugin to the `plugins.json` file at the root of this repository.
This file is a list of all the available plugins and multiple version can coexist.
To add a plugin, add an entry to the `plugins` in.


    "myplugin@1.0.0" : "plugins/myplugin/1.0.0/myplugin.cspm.json"


Then, at the path declared create the given file (or copy an existing one and modify as needed)

```json
{
    "name": "myplugin",
    "libname": "libmyplugin",
    "version": "1.0.0",
    "short_description": "Miscellaneous plugins",
    "long_description": "Miscellaneous plugins, ...",
    "csound_version": "6.14",
    "binaries": {
        "linux": {
            "url": "linux/limyplugin.so", 
            "build_platform": "Ubuntu 16.04"
        },
        "macos": {
            "url": "macos/libmyplugin.dylib",
            "build_platform": "10.14.0"
        },
        "windows": {
            "url": "windows/libmyplugin.dll",
            "build_platform": "Windows 10"
        }
    },
    "opcodes": [
        "plugin1", "plugin2"
    ],
    "author": "John Doe",
    "email": "john.doe@email.com",
    "manual": "myplugin.zip"
}

```

Then copy the binaries for the declared platforms to the folder `plugins/myplugins/<version>/linux`, 
`plugins/myplugins/<version>/macos`, `plugins/myplugins/<version>/windows`, as needed.
If a plugin is not available under a given platform don't include an entry for that platform
(see the plugin `emplugins/jsfx` for an example where windows is not supported)

 
[cspm]: https://github.com/csound-plugins/cspm