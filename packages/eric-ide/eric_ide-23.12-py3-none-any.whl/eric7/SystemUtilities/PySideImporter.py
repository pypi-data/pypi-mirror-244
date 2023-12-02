# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module to check for the presence of PySide2/PySide6 by importing it.
"""

import importlib
import sys

if __name__ == "__main__":
    pySideVariant = "2"
    if len(sys.argv) == 2:
        pySideVariant = sys.argv[1].replace("--variant=", "")

    if pySideVariant == "1":
        # no PySide support anymore
        ret = 1

    elif pySideVariant == "2":
        ret = 1 if importlib.util.find_spec("PySide") is None else 0

    elif pySideVariant == "6":
        ret = 1 if importlib.util.find_spec("PySide6") is None else 0

    else:
        ret = 1

    sys.exit(ret)
