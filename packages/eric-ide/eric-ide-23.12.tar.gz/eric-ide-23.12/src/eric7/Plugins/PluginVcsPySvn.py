# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the PySvn version control plugin.
"""

import contextlib
import importlib
import os

from PyQt6.QtCore import QCoreApplication, QObject

from eric7 import Preferences
from eric7.EricWidgets.EricApplication import ericApp
from eric7.Plugins.VcsPlugins.vcsPySvn.SvnUtilities import getConfigPath, getServersPath
from eric7.Preferences.Shortcuts import readShortcuts
from eric7.UI import Info

# Start-Of-Header
__header__ = {
    "name": "PySvn Plugin",
    "author": "Detlev Offenbach <detlev@die-offenbachs.de>",
    "autoactivate": False,
    "deactivateable": True,
    "version": Info.VersionOnly,
    "pluginType": "version_control",
    "pluginTypename": "PySvn",
    "className": "VcsPySvnPlugin",
    "packageName": "__core__",
    "shortDescription": "Implements the PySvn version control interface.",
    "longDescription": """This plugin provides the PySvn version control interface.""",
    "pyqtApi": 2,
}
# End-Of-Header

error = ""  # noqa: U200


def exeDisplayData():
    """
    Public method to support the display of some executable info.

    @return dictionary containing the data to be shown
    """
    try:
        import pysvn  # __IGNORE_WARNING_I10__

        try:
            text = os.path.dirname(pysvn.__file__)
        except AttributeError:
            text = "PySvn"
        version = ".".join([str(v) for v in pysvn.version])
    except ImportError:
        text = "PySvn"
        version = ""

    data = {
        "programEntry": False,
        "header": QCoreApplication.translate(
            "VcsPySvnPlugin", "Version Control - Subversion (pysvn)"
        ),
        "text": text,
        "version": version,
    }

    return data


def getVcsSystemIndicator():
    """
    Public function to get the indicators for this version control system.

    @return dictionary with indicator as key and a tuple with the vcs name
        (string) and vcs display string (string)
    """
    return {
        ".svn": (__header__["pluginTypename"], displayString()),
        "_svn": (__header__["pluginTypename"], displayString()),
    }


def displayString():
    """
    Public function to get the display string.

    @return display string (string)
    """
    if importlib.util.find_spec("pysvn") is None:
        return ""
    else:
        return QCoreApplication.translate("VcsPySvnPlugin", "Subversion (pysvn)")


subversionCfgPluginObject = None


def createConfigurationPage(configDlg):  # noqa: U100
    """
    Module function to create the configuration page.

    @param configDlg reference to the configuration dialog (QDialog)
    @return reference to the configuration page
    """
    from eric7.Plugins.VcsPlugins.vcsPySvn.ConfigurationPage.SubversionPage import (
        SubversionPage,
    )

    global subversionCfgPluginObject

    if subversionCfgPluginObject is None:
        subversionCfgPluginObject = VcsPySvnPlugin(None)
    page = SubversionPage(subversionCfgPluginObject)
    return page


def getConfigData():
    """
    Module function returning data as required by the configuration dialog.

    @return dictionary with key "zzz_subversionPage" containing the relevant
    data
    """
    return {
        "zzz_subversionPage": [
            QCoreApplication.translate("VcsPySvnPlugin", "Subversion"),
            os.path.join(
                "VcsPlugins", "vcsPySvn", "icons", "preferences-subversion.svg"
            ),
            createConfigurationPage,
            "vcsPage",
            None,
        ],
    }


def prepareUninstall():
    """
    Module function to prepare for an uninstallation.
    """
    if not ericApp().getObject("PluginManager").isPluginLoaded("PluginVcsSubversion"):
        Preferences.getSettings().remove("Subversion")


class VcsPySvnPlugin(QObject):
    """
    Class implementing the PySvn version control plugin.
    """

    def __init__(self, ui):
        """
        Constructor

        @param ui reference to the user interface object (UI.UserInterface)
        """
        from eric7.Plugins.VcsPlugins.vcsPySvn.ProjectHelper import PySvnProjectHelper

        super().__init__(ui)
        self.__ui = ui

        self.__subversionDefaults = {
            "StopLogOnCopy": 1,
            "LogLimit": 20,
        }

        self.__projectHelperObject = PySvnProjectHelper(None, None)
        with contextlib.suppress(KeyError):
            ericApp().registerPluginObject(
                __header__["pluginTypename"],
                self.__projectHelperObject,
                __header__["pluginType"],
            )
        readShortcuts(pluginName=__header__["pluginTypename"])

    def getProjectHelper(self):
        """
        Public method to get a reference to the project helper object.

        @return reference to the project helper object
        """
        return self.__projectHelperObject

    def initToolbar(self, ui, toolbarManager):
        """
        Public slot to initialize the VCS toolbar.

        @param ui reference to the main window (UserInterface)
        @param toolbarManager reference to a toolbar manager object
            (EricToolBarManager)
        """
        if self.__projectHelperObject:
            self.__projectHelperObject.initToolbar(ui, toolbarManager)

    def activate(self):
        """
        Public method to activate this plugin.

        @return tuple of reference to instantiated viewmanager and
            activation status (boolean)
        """
        from eric7.Plugins.VcsPlugins.vcsPySvn.subversion import Subversion

        self.__object = Subversion(self, self.__ui)

        tb = self.__ui.getToolbar("vcs")[1]
        tb.setVisible(False)
        tb.setEnabled(False)

        tb = self.__ui.getToolbar("pysvn")[1]
        tb.setVisible(Preferences.getVCS("ShowVcsToolbar"))
        tb.setEnabled(True)

        return self.__object, True

    def deactivate(self):
        """
        Public method to deactivate this plugin.
        """
        self.__object = None

        tb = self.__ui.getToolbar("pysvn")[1]
        tb.setVisible(False)
        tb.setEnabled(False)

        tb = self.__ui.getToolbar("vcs")[1]
        tb.setVisible(Preferences.getVCS("ShowVcsToolbar"))
        tb.setEnabled(True)

    def getPreferences(self, key):
        """
        Public method to retrieve the various settings.

        @param key the key of the value to get
        @return the requested refactoring setting
        """
        if key in ["StopLogOnCopy"]:
            return Preferences.toBool(
                Preferences.getSettings().value(
                    "Subversion/" + key, self.__subversionDefaults[key]
                )
            )
        elif key in ["LogLimit"]:
            return int(
                Preferences.getSettings().value(
                    "Subversion/" + key, self.__subversionDefaults[key]
                )
            )
        elif key in ["Commits"]:
            return Preferences.toList(
                Preferences.getSettings().value("Subversion/" + key)
            )
        else:
            return Preferences.getSettings().value("Subversion/" + key)

    def setPreferences(self, key, value):
        """
        Public method to store the various settings.

        @param key the key of the setting to be set
        @param value the value to be set
        """
        Preferences.getSettings().setValue("Subversion/" + key, value)

    def getServersPath(self):
        """
        Public method to get the filename of the servers file.

        @return filename of the servers file (string)
        """
        return getServersPath()

    def getConfigPath(self):
        """
        Public method to get the filename of the config file.

        @return filename of the config file (string)
        """
        return getConfigPath()

    def prepareUninstall(self):
        """
        Public method to prepare for an uninstallation.
        """
        ericApp().unregisterPluginObject(__header__["pluginTypename"])

    def prepareUnload(self):
        """
        Public method to prepare for an unload.
        """
        if self.__projectHelperObject:
            self.__projectHelperObject.removeToolbar(
                self.__ui, ericApp().getObject("ToolbarManager")
            )
        ericApp().unregisterPluginObject(__header__["pluginTypename"])
