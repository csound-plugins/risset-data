![risset](assets/risset-title-white.png)


# risset - a csound package manager - Plugin Index Repository

This repository hosts the index for all csound plugins defined in [risset], the csound package manager.

This repository does not host any source code or binaries. Each plugin is defined within a git repository and cloned by *risset* itself.


## Installing plugins

In order to install and manage the plugins defined here, `risset` needs to be installed:


```bash
pip install risset
```

This will install the script "risset" into your path


### Linux

In certain linux distributions it is not allowed to install packages to the
system python. In that case the recommended way is to install risset within
its own virtual environment. On ubuntu this can be done via `pipx`:

```bash
sudo apt install pipx
pipx install risset
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
  "author": "Alice",
  "email": "alice@email.com",
  "license": "LGPL",
  "repository": "https://github.com/alice/myplugin",
  "binaries": [
    {
      "platform": "linux-x86_64",
      "url": "https://github.com/alice/releases/myplugin-csound6.zip",
      "extractpath": "myplugin.so",
      "csound_version": ">=6.17<7.0"
    },
    {
      "platform": "linux-x86_64",
      "url": "https://github.com/alice/releases/myplugin-csound7.zip",
      "extractpath": "myplugin.so",
      "csound_version": ">=7.0"
    },
    {
      "platform": "macos-arm64",
      "url": "https://github.com/alice/releases/myplugin-csound6.zip",
      "extractpath": "myplugin.dylib",
      "csound_version": ">=6.17<7.0"
    },
    {
      "platform": "macos-arm64",
      "url": "https://github.com/alice/releases/myplugin-csound7.zip",
      "extractpath": "myplugin.dylib",
      "csound_version": ">=7.0"
    },
    {
      "platform": "windows-x86_64",
      "url": "https://github.com/alice/releases/myplugin-csound6.zip",
      "extractpath": "myplugin.dll",
      "csound_version": ">=6.17<7.0"
    },
    {
      "platform": "windows-x86_64",
      "url": "https://github.com/alice/releases/myplugin-csound7.zip",
      "extractpath": "myplugin.dll",
      "csound_version": ">=7.0"
    },
  ]
}

```

Things to notice:

* A plugin must include **at least one binary**. *risset* distributes only binaries so you need to build binaries and provide an URL from which the binary can be downloaded. A good place to put the binaries is as a release in the git repository of the plugin.
* The url of a binary can point to the binary itself (a file with a .so, .dll or .dylib extension), or a .zip file. In this latter case, the binary needs to include an `extractpath` tag besides the url, pointing at the actual binary
within the .zip structure, as in the example above.
* It is highly recommended to add one manual page per opcode. These will be indexed and used to build a global manual for all plugins defined within risset. Use this as a template: https://github.com/csound-plugins/csound-plugins/blob/master/src/else/doc/zeroarray.md
* The doc folder with the manual pages for each opcode is declared as a relative
path to the `risset.json` file. By default risset searches for a "doc" folder in the same directory as
the risset.json file. It should include one manual file for each opcode, in markdown format.
 Use this as a template: https://github.com/csound-plugins/csound-plugins/blob/master/src/else/doc/zeroarray.md


[risset]: https://github.com/csound-plugins/risset
