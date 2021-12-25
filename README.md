![risset](assets/risset-title-white.png)


# risset - a csound package manager - Plugin Index Repository

This repository hosts the index for all csound plugins defined in [risset], the csound package manager.

This repository does not host any source code or binaries. Each plugin is defined within a git repository and cloned by *risset* itself. 


## Installing plugins

In order to install and manage the plugins defined here, `risset` needs to be installed:

```bash
pip3 install risset
```

Alternatively the latest pushed version can be installed via `git`

```bash
git clone https://github.com/csound-plugins/risset
cd risset
python3 setup.py install
```

## Usage

```bash
risset list          # list all available plugins
risset install poly  # install/update the poly plugin
```

## Documentation

Manual pages for each opcode can be found here: https://csound-plugins.github.io/risset-docs/


## Contributing

In order to add a plugin or a collection of plugins to this repository, fork this repository and add your plugin to the indexfile, `rissetindex.json` at the root of this repo.


### Anatomy of a plugin declaration

This is an example of a plugin named "myplugin", developed by "Alice". The folder structure could be:

```
myplugin/
  src/
    myplugin.c
  doc/
    opcode1.md
    opcode2.md
  examples/
    opcode1.csd
    opcode2.csd
  CMakeLists.txt
  risset.json
```
  
The source code or the cmake file are not needed, they are included just to show
that it is possible to include the risset definition within the repository
of the plugin's source itself.
  
The content of `risset.json` should be:

```json
{
  "name": "myplugin",
  "opcodes": [
    "opcode1",
    "opcode2"
  ],
  "version": "0.1.0",
  "short_description": "Test opcodes",
  "long_description": "A set of opcodes to test risset",
  "csound_version": "6.17",
  "author": "Alice",
  "email": "alice@email.com",
  "license": "LGPL",
  "repository": "https://github.com/alice/myplugin",
  "doc_folder": "doc",
  "binaries": {
    "linux": {
      "url": "https://github.com/alice/myplugin/releases/download/v0.1.0/myplugin.zip",
      "extractpath": "myplugin.so",
      "build_platform": "Ubuntu 18.04"
    },
    "macos": {
      "url": "https://github.com/alice/myplugin/releases/download/v0.1.0/myplugin.zip",
	  "extractpath": "myplugin.dylib",
      "build_platform": "10.14.0"
    },
    "windows": {
      "url": "https://github.com/alice/myplugin/releases/download/v0.1.0/myplugin.dll",
	  "build_platform": "Windows 10"
    }
  }
}

```

Things to notice:

* A plugin must include **at least one binary**. *risset* distributes only binaries so you need to build binaries and provide an URL from which the binary can be downloaded. A good place to put the binaries is as a release in the git repository of the plugin.
* The url of a binary can point to the binary itself (a file with a .so, .dll or .dylib extension), or a .zip file. In this latter case, the binary needs to include an `extractpath` tag besides the url, pointing at the actual binary
within the .zip structure, as in the example above.
* The `build_platform` tag is just for information to the user, indicating which platform was used to build the binary.
* It is highly recommended to add one manual page per opcode. These will be indexed and used to build a global manual for all plugins defined within risset. Use this as a template: https://github.com/csound-plugins/csound-plugins/blob/master/src/else/doc/zeroarray.md
* The doc folder with the manual pages for each opcode is declared as a relative 
path to the `risset.json` file. It should include one manual file for each opcode. 
 Use this as a template: https://github.com/csound-plugins/csound-plugins/blob/master/src/else/doc/zeroarray.md


[risset]: https://github.com/csound-plugins/risset
