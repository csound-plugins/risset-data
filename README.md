![risset](assets/risset-title.png)


# risset - a csound package manager - Plugin Repository

This is a repository for csound plugins to be used in coordination
with [risset], the csound package manager.

This repository is **ONLY** for storage of binaries, not for source code


## Installing plugins

In order to install and manage the plugins defined here, use the utility `risset`. To
install `risset` do either

```bash
pip3 install risset
```

or install it via `git`

```bash
git clone https://github.com/csound-plugins/risset
cd risset
python3 setup.py install
```

Then you can use it directly:

```bash
risset list          # list all available plugins
risset install poly  # install/update the poly plugin
```


## Contributing

In order to add a plugin or a collection of plugins to this repository, fork
this repository and create a PR.

### Anatomy of a plugin declaration

Example of a plugin named "myplugin", developed by "Alice" (NB: the name of the manifest can be
any name with the .json suffix). The folder structure could be:

```
/
  plugins/
    alice/
      1.0.0/
        myplugin/
          manifest.json
          myplugin.so
          myplugin.dll
          myplugin.dylib
          doc/
            opcode1.md
            opcode2.md
            examples/
              opcode1.csd
              opcode2.csd
```

How the folder is structured is acutally free for the developer to decide. What Alice needs to remember is that **the manifest is declared relative to the plugins.json file and the binaries declared in the manifest are relative to the manifest itself**

First alice needs to add her plugin to the `plugins.json` file at the root of this repository.
This file is a list of all the available plugins and multiple version can coexist.
To add a plugin, she adds an entry to the `plugins` in.

    "myplugin@1.0.0" : "plugins/alice/1.0.0/myplugin/manifest.json"

Then, at the path declared above she creates the manifest file


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
            "url": "libmyplugin.so",
            "build_platform": "Ubuntu 16.04"
        },
        "macos": {
            "url": "libmyplugin.dylib",
            "build_platform": "10.14.0"
        },
        "windows": {
            "url": "libmyplugin.dll",
            "build_platform": "Windows 10"
        }
    },
    "opcodes": [
        "opcode1", "opcode2"
    ],
    "author": "Alice",
    "email": "alice@email.com"
}

```

Then she copies the binaries for the declared platforms to the location indicated in the manifest file. In this case the files are declared in the same folder as the manifest itself.

**NB: If a plugin is not available under a given platform don't include an entry for that
platform (see the plugin `emplugins/jsfx` for an example where windows is not supported)**

[risset]: https://github.com/csound-plugins/risset
