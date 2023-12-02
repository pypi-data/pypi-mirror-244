# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing an importer for HTML bookmark files.
"""

import os

from PyQt6.QtCore import QCoreApplication, QDate, Qt

from eric7.EricGui import EricPixmapCache

from .BookmarksImporter import BookmarksImporter


def getImporterInfo(sourceId):
    """
    Module function to get information for the given HTML source id.

    @param sourceId id of the browser ("chrome" or "chromium")
    @return tuple with an icon (QPixmap), readable name (string), name of
        the default bookmarks file (string), an info text (string),
        a prompt (string) and the default directory of the bookmarks file
        (string)
    @exception ValueError raised to indicate an invalid browser ID
    """
    if sourceId != "html":
        raise ValueError("Unsupported browser ID given ({0}).".format(sourceId))

    return (
        EricPixmapCache.getPixmap("html"),
        "HTML Netscape Bookmarks",
        QCoreApplication.translate("HtmlImporter", "HTML Netscape Bookmarks")
        + " (*.htm *.html)",
        QCoreApplication.translate(
            "HtmlImporter",
            """You can import bookmarks from any browser that supports"""
            """ HTML exporting. This file has usually the extension"""
            """ .htm or .html.""",
        ),
        QCoreApplication.translate(
            "HtmlImporter", """Please choose the file to begin importing bookmarks."""
        ),
        "",
    )


class HtmlImporter(BookmarksImporter):
    """
    Class implementing the HTML bookmarks importer.
    """

    def __init__(self, sourceId="", parent=None):
        """
        Constructor

        @param sourceId source ID (defaults to "")
        @type str (optional)
        @param parent reference to the parent object (defaults to None)
        @type QObject (optional)
        """
        super().__init__(sourceId, parent)

        self.__fileName = ""
        self.__inFile = None

    def setPath(self, path):
        """
        Public method to set the path of the bookmarks file or directory.

        @param path bookmarks file or directory (string)
        """
        self.__fileName = path

    def open(self):
        """
        Public method to open the bookmarks file.

        @return flag indicating success (boolean)
        """
        if not os.path.exists(self.__fileName):
            self._error = True
            self._errorString = self.tr("File '{0}' does not exist.").format(
                self.__fileName
            )
            return False
        return True

    def importedBookmarks(self):
        """
        Public method to get the imported bookmarks.

        @return imported bookmarks (BookmarkNode)
        """
        from ..BookmarkNode import BookmarkNode
        from ..NsHtmlReader import NsHtmlReader

        reader = NsHtmlReader()
        importRootNode = reader.read(self.__fileName)

        importRootNode.setType(BookmarkNode.Folder)
        if self._id == "html":
            importRootNode.title = self.tr("HTML Import")
        else:
            importRootNode.title = self.tr("Imported {0}").format(
                QDate.currentDate().toString(Qt.DateFormat.ISODate)
            )
        return importRootNode


def createImporter(sourceId="", parent=None):
    """
    Constructor

    @param sourceId source ID (defaults to "")
    @type str (optional)
    @param parent reference to the parent object (defaults to None)
    @type QObject (optional)
    @return reference to the instantiated importer object
    @rtype HtmlImporter
    """
    return HtmlImporter(sourceId=sourceId, parent=parent)
