# This file is placed in the Public Domain.
#
# pylint: disable=C0103,C0116,E0402


"available modules"


import sys
import os


def mod(event):
    modules = sys.modules.get("sbn.modules", None)
    if not modules:
        event.reply("modules not found")
        return
    modlist = [
               x[:-3] for x in os.listdir(modules.__path__[0])
               if x.endswith(".py")
               and x not in ["__main__.py", "__init__.py"]
              ]
    event.reply(",".join(sorted(modlist)))
