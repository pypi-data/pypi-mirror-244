# -*- coding: utf-8 -*-

# Copyright (c) 2004 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a Perl lexer with some additional methods.
"""

import contextlib

from PyQt6.Qsci import QsciLexerPerl

from eric7 import Preferences

from .Lexer import Lexer


class LexerPerl(Lexer, QsciLexerPerl):
    """
    Subclass to implement some additional lexer dependant methods.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent parent widget of this lexer
        """
        QsciLexerPerl.__init__(self, parent)
        Lexer.__init__(self)

        self.commentString = "#"

        self.keywordSetDescriptions = [
            self.tr("Keywords"),
        ]

    def initProperties(self):
        """
        Public slot to initialize the properties.
        """
        self.setFoldComments(Preferences.getEditor("PerlFoldComment"))
        self.setFoldCompact(Preferences.getEditor("AllFoldCompact"))
        with contextlib.suppress(AttributeError):
            self.setFoldPackages(Preferences.getEditor("PerlFoldPackages"))
            self.setFoldPODBlocks(Preferences.getEditor("PerlFoldPODBlocks"))
        with contextlib.suppress(AttributeError):
            self.setFoldAtElse(Preferences.getEditor("PerlFoldAtElse"))

    def autoCompletionWordSeparators(self):
        """
        Public method to return the list of separators for autocompletion.

        @return list of separators (list of strings)
        """
        return ["::", "->"]

    def isCommentStyle(self, style):
        """
        Public method to check, if a style is a comment style.

        @param style style to check (integer)
        @return flag indicating a comment style (boolean)
        """
        return style in [QsciLexerPerl.Comment]

    def isStringStyle(self, style):
        """
        Public method to check, if a style is a string style.

        @param style style to check (integer)
        @return flag indicating a string style (boolean)
        """
        return style in [
            QsciLexerPerl.DoubleQuotedHereDocument,
            QsciLexerPerl.DoubleQuotedString,
            QsciLexerPerl.QuotedStringQ,
            QsciLexerPerl.QuotedStringQQ,
            QsciLexerPerl.QuotedStringQR,
            QsciLexerPerl.QuotedStringQW,
            QsciLexerPerl.QuotedStringQX,
            QsciLexerPerl.SingleQuotedHereDocument,
            QsciLexerPerl.SingleQuotedString,
        ]

    def defaultKeywords(self, kwSet):
        """
        Public method to get the default keywords.

        @param kwSet number of the keyword set (integer)
        @return string giving the keywords (string) or None
        """
        return QsciLexerPerl.keywords(self, kwSet)


def createLexer(variant="", parent=None):  # noqa: U100
    """
    Function to instantiate a lexer object.

    @param variant name of the language variant
    @type str
    @param parent parent widget of this lexer
    @type QObject
    @return instantiated lexer object
    @rtype LexerPerl
    """
    return LexerPerl(parent=parent)
