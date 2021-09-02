#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
import json
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Optional


settings = {'debug': False}

ROOTFOLDER = Path(sys.argv[0]).absolute().parent.parent


class IndexParseError(Exception): pass
class ParseError(Exception): pass


def errormsg(*msgs):
    print("ERROR:", *msgs, file=sys.stderr)


def debug(*msgs):
    if settings['debug']:
        print("DEBUG:", *msgs, file=sys.stderr)


def resolve_relative_path(relpath: str, basepath: str) -> Path:
    base = Path(basepath).absolute()
    return base / relpath


@dataclass
class Manifest:
    name: str
    path: Path
    manifest: dict


def parse_manifest(path: Path) -> Manifest:
    d = json.load(open(path.as_posix()))
    return Manifest(name=d['name'], path=path, manifest=d)


def parse_index(indexfile: Path) -> Dict[str, Manifest]:
    try:
        d = json.load(open(indexfile.as_posix()))
    except json.JSONDecodeError as e:
        print(f"Couln not parse indexfile: {indexfile}")
        errormsg(str(e))
        raise IndexParseError()

    if 'plugins' not in d:
        raise IndexParseError("index malformed, it has no key 'plugins'")

    plugins = {}
    for pluginkey, manifesturl in d['plugins'].items():
        if "@" in pluginkey:
            pluginname, version = pluginkey.split("@")
        else:
            pluginname = pluginkey
            version = "0.0.0"
        manifestpath = resolve_relative_path(manifesturl, indexfile.parent)
        if not manifestpath.exists():
            errormsg(f"Manifest for plugin {pluginname} not found at defined path, skipping")
            errormsg(f"    Path: {str(manifestpath)}")
            continue
        try:
            manifest = parse_manifest(manifestpath)
        except json.JSONDecodeError as e:
            errormsg(f"Could not parse manifest {pluginname}: {str(manifestpath)}")
            errormsg(str(e))
            continue
        plugins[pluginname] = manifest
    return plugins


def find_doc_folder(manifest: Manifest) -> Optional[Path]:
    relative_doc_folder = manifest.manifest.get('doc')
    if relative_doc_folder:
        doc_folder = resolve_relative_path(relative_doc_folder, manifest.path.as_posix())
        if not doc_folder.exists():
            raise OSError("doc folder does not exist, declared as {doc_folder} in manifest")
        return doc_folder
    # No declared doc folder, use default
    default_doc_folder = manifest.path.parent / "doc"
    if default_doc_folder.exists():
        return default_doc_folder
    return None


def copy_recursive(src: Path, dest: Path) -> None:
    if not dest.exists():
        raise OSError(f"Destination path ({str(dest)}) does not exist")
    if not dest.is_dir():
        raise OSError(f"Destination path (str{dest}) should be a directory")

    if src.is_dir():
        debug(f"Copying all files under {str(src)} to {str(dest)}")
        for f in src.glob("*"):
            debug("    ", str(f))
            if f.is_dir():
                shutil.copytree(f.absolute().as_posix(), dest.as_posix())
            else:
                shutil.copy(f.as_posix(), dest.as_posix())
    else:
        debug(f"Copying file {str(src)} to {str(dest)}")
        shutil.copy(src.as_posix(), dest.as_posix())


def compile_docs(dest: Path, manifests: List[Manifest]) -> None:
    """
    * Prepare the folder structure
    * Copy ALL documentation to a destination folder (all .md files)
    * Collect all assets
    """
    dest = dest.expanduser().absolute()

    if dest.exists():
        debug(f"Removing existing doc folder: {str(dest)}")
        shutil.rmtree(dest.as_posix())

    css_folder = dest / "css"
    opcodes_folder = dest / "opcodes"
    opcodes_assets_folder = opcodes_folder / "assets"

    for folder in [dest, css_folder, opcodes_folder, opcodes_assets_folder]:
        folder.mkdir(exist_ok=True, parents=True)

    # copy .css file
    shutil.copy(ROOTFOLDER/"assets"/"syntax-highlighting.css", css_folder)

    for manifest in manifests:
        doc_folder = find_doc_folder(manifest)
        if doc_folder is None:
            debug(f"No docs found for plugin: {manifest.name}")
            continue

        docs = doc_folder.glob("*.md")
        if not docs:
            debug(f"No documentation found in {doc_folder}")
            continue

        debug(f"Copying docs to {opcodes_folder}")
        for doc in docs:
            debug(" copying", str(doc))
            shutil.copy(doc.as_posix(), opcodes_folder.as_posix())

        # copy any assets
        source_assets_folder = doc_folder / "assets"
        if source_assets_folder.exists() and source_assets_folder.is_dir():
            debug(f"Copying assets for plugin {manifest.name}")
            copy_recursive(source_assets_folder, opcodes_assets_folder)
        else:
            debug(f"No assets to copy for plugin {manifest.name}")


def index_manpages(manifests:List[Manifest]) -> Dict[str, Path]:
    """
    Index all manifests, return a dict mapping each opcode to its manpage

    We assume that the manpage has the same name as the opcode (case-insensitive)
    """
    manpages = {}
    for manifest in manifests:
        doc_folder = find_doc_folder(manifest)
        if not doc_folder:
            debug(f"No docs for plugin {manifest.name}")
            continue
        opcodes = manifest.manifest.get("opcodes")
        if not opcodes:
            debug(f"No opcodes defined in manifest for plugin {manifest.name}")
            continue
        mdfiles = list(doc_folder.glob("*.md"))
        for opcode in opcodes:
            for mdfile in mdfiles:
                if mdfile.stem.lower() == opcode.lower():
                    manpages[opcode] = mdfile.absolute()
                    break
            else:
                debug(f"No manpage for opcode {opcode} (plugin: {manifest.name})")
                debug("    .md files found: ", mdfiles)
    return manpages


def get_abstract(manpage: Path, opcode: str) -> str:
    """

    Args:
        manpage: the path to the manpage for the given opcode
        opcode: the name of the opcode

    Returns:
        the abstract. Can be an empty string if the opcode has no abstract

    Raises:
        ParseError if the manpage can't be parsed
    """
    text = open(manpage).read()
    if "# Abstract" in text:
        # the abstract would be all the text between # Abstract and the next #tag
        debug(f"get_abstract: manpage for opcode {opcode} has abstract")
        it = iter(text.splitlines())
        for line in it:
            if not "# Abstract" in line:
                continue
            for line in it:
                line = line.strip()
                if not line:
                    continue
                return line if not line.startswith("#") else ""
        debug(f"No abstract in manpage file {manpage}")
        return ""
    # no Abstract tag, so abstract is the text between the title and the text tag
    debug(f"get_abstract: manpage for opcode {opcode} has no # Abstract tag")
    it = iter(text.splitlines())
    for line in it:
        line = line.strip()
        if not line:
            continue
        if not line.startswith("#"):
            raise ParseError(f"Expected title, got {line}")
        parts = line.split()
        if len(parts) != 2:
            raise ParseError("Could not parse title, expected line of the form '# opcode'")
        if parts[1].lower() != opcode.lower():
            raise ParseError(f"Expected title ({parts[1]} to be the same as opcode name ({opcode})")
        for line in it:
            line = line.strip()
            if not line:
                continue
            return line if not line.startswith("#") else ""
        debug(f"No abstract in manpage file {manpage}")
        return ""


def generate_index(manifests:List[Manifest], manpages: Dict[str, Path],
                   indexfile:str=None, create_readme=True) -> None:
    lines = []
    _ = lines.append
    _("# Csound Plugins")
    _("")
    manifests.sort(key=lambda manifest:manifest.name)
    for manifest in manifests:
        opcodes = manifest.manifest.get('opcodes')
        if not opcodes:
            continue
        _(f"## {manifest.name}")
        _("")
        _(manifest.manifest.get("short_description"))
        _("")

        opcodes.sort()
        for opcode in opcodes:
            manpage = manpages.get(opcode)
            if not manpage:
                debug(f"opcode {opcode} has no manpage")
                continue
            try:
                abstract = get_abstract(manpage, opcode)
            except ParseError as err:
                errormsg(f"Could not get abstract for opcode {opcode}", str(err))
                continue
            _(f"  * [{opcode}](opcodes/{opcode}.md): {abstract}")

        _("")

    if not indexfile:
        indexfile = ROOTFOLDER / "docs" / "index.md"
    print("\n".join(lines))

    with open(indexfile, "w") as f:
        f.write("\n".join(lines))

    if create_readme:
        shutil.copy(indexfile, indexfile.parent/"README.md")


def build_mkdocs():
    mkdocs = shutil.which("mkdocs")
    if not mkdocs:
        errormsg("Asked to build html documentation, but mkdocs was not found in the path")
        return
    subprocess.call([mkdocs, "build"])


##  -------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--indexfile", default="", help="Location of the plugins.json file")
parser.add_argument("--debug", action="store_true")
parser.add_argument("--html", action="store_true",
                    help="Build html documentation. This requires mkdocs to be installed")
args = parser.parse_args()

if args.debug:
    settings['debug'] = True

if args.indexfile:
    indexfile:Path = Path(args.indexfile).absolute()
else:
    indexfile:Path = ROOTFOLDER / "plugins.json"

if not indexfile.exists():
    errormsg(f"Index file {str(indexfile)} does not exist")
    sys.exit(-1)

debug(f"Indexfile: {str(indexfile)}")

plugins = parse_index(indexfile)
manifests = list(plugins.values())
docs_folder = indexfile.parent/"docs"
manpages = index_manpages(manifests)
compile_docs(docs_folder, manifests)
generate_index(manifests, manpages)

if args.html:
    build_mkdocs()
