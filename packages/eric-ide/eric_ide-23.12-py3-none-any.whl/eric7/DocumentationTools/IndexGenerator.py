# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the index generator for the builtin documentation
generator.
"""

import os
import sys

from eric7.SystemUtilities import FileSystemUtilities

from . import TemplatesListsStyleCSS


class IndexGenerator:
    """
    Class implementing the index generator for the builtin documentation
    generator.
    """

    def __init__(self, outputDir):
        """
        Constructor

        @param outputDir The output directory for the files
        @type str
        """
        self.outputDir = outputDir
        self.packages = {
            "00index": {"description": "", "subpackages": {}, "modules": {}}
        }
        self.remembered = False

    def remember(self, file, moduleDocument, basename=""):
        """
        Public method to remember a documentation file.

        @param file The filename to be remembered. (string)
        @param moduleDocument The ModuleDocument object containing the
            information for the file.
        @param basename The basename of the file hierarchy to be documented.
            The basename is stripped off the filename if it starts with
            the basename.
        """
        self.remembered = True
        if basename:
            file = file.replace(basename, "")

        if "__init__" in file:
            dirName = os.path.dirname(file)
            udir = os.path.dirname(dirName)
            if udir:
                upackage = udir.replace(os.sep, ".")
                try:
                    elt = self.packages[upackage]
                except KeyError:
                    elt = self.packages["00index"]
            else:
                elt = self.packages["00index"]
            package = dirName.replace(os.sep, ".")
            elt["subpackages"][package] = moduleDocument.shortDescription()

            self.packages[package] = {
                "description": moduleDocument.description(),
                "subpackages": {},
                "modules": {},
            }

            if moduleDocument.isEmpty():
                return

        package = os.path.dirname(file).replace(os.sep, ".")
        try:
            elt = self.packages[package]
        except KeyError:
            elt = self.packages["00index"]
        elt["modules"][moduleDocument.name()] = moduleDocument.shortDescription()

    def __writeIndex(self, packagename, package, newline=None):
        """
        Private method to generate an index file for a package.

        @param packagename The name of the package. (string)
        @param package A dictionary with information about the package.
        @param newline newline character to be used (string)
        @return The name of the generated index file.
        """
        if packagename == "00index":
            f = os.path.join(self.outputDir, "index")
            title = "Table of contents"
        else:
            f = os.path.join(self.outputDir, "index-{0}".format(packagename))
            title = packagename

        filename = FileSystemUtilities.joinext(f, ".html")

        subpackages = ""
        modules = ""

        # 1) subpackages
        if package["subpackages"]:
            subpacks = package["subpackages"]
            names = sorted(subpacks.keys())
            lst = []
            for name in names:
                link = FileSystemUtilities.joinext("index-{0}".format(name), ".html")
                lst.append(
                    TemplatesListsStyleCSS.indexListEntryTemplate.format(
                        **{
                            "Description": subpacks[name],
                            "Name": name.split(".")[-1],
                            "Link": link,
                        }
                    )
                )
            subpackages = TemplatesListsStyleCSS.indexListPackagesTemplate.format(
                **{
                    "Entries": "".join(lst),
                }
            )

        # 2) modules
        if package["modules"]:
            mods = package["modules"]
            names = sorted(mods.keys())
            lst = []
            for name in names:
                link = FileSystemUtilities.joinext(name, ".html")
                nam = name.split(".")[-1]
                if nam == "__init__":
                    nam = name.split(".")[-2]
                lst.append(
                    TemplatesListsStyleCSS.indexListEntryTemplate.format(
                        **{
                            "Description": mods[name],
                            "Name": nam,
                            "Link": link,
                        }
                    )
                )
            modules = TemplatesListsStyleCSS.indexListModulesTemplate.format(
                **{
                    "Entries": "".join(lst),
                }
            )

        doc = (
            TemplatesListsStyleCSS.headerTemplate.format(**{"Title": title})
            + TemplatesListsStyleCSS.indexBodyTemplate.format(
                **{
                    "Title": title,
                    "Description": package["description"],
                    "Subpackages": subpackages,
                    "Modules": modules,
                }
            )
            + TemplatesListsStyleCSS.footerTemplate
        )

        with open(filename, "w", encoding="utf-8", newline=newline) as f:
            f.write(doc)

        return filename

    def writeIndices(self, basename="", newline=None):
        """
        Public method to generate all index files.

        @param basename The basename of the file hierarchy to be documented.
            The basename is stripped off the filename if it starts with
            the basename.
        @param newline newline character to be used (string)
        """
        if not self.remembered:
            sys.stderr.write("No index to generate.\n")
            return

        if basename:
            basename = basename.replace(os.sep, ".")
            if not basename.endswith("."):
                basename = "{0}.".format(basename)
        for package, element in list(self.packages.items()):
            try:
                if basename:
                    package = package.replace(basename, "")
                out = self.__writeIndex(package, element, newline)
            except OSError as v:
                sys.stderr.write("{0} error: {1}\n".format(package, v[1]))
            except Exception as ex:
                sys.stderr.write(
                    "{0} error writing index: {1}\n".format(package, str(ex))
                )
                raise
            else:
                if out:
                    sys.stdout.write("{0} ok\n".format(out))

        sys.stdout.write("Indices written.\n")
        sys.stdout.flush()
        sys.stderr.flush()
