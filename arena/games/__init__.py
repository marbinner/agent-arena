"""Game package auto-discovery.

Rather than manually editing this file every time a new game is added, we
automatically import any modules in this package that define subclasses of the
``Game`` base class.  This keeps merge conflicts to a minimum because new games
only need to add a new module and do not modify shared files.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil

from ..base import Game

__all__: list[str] = []

for finder, name, ispkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{name}")
    for attr_name, attr in vars(module).items():
        if inspect.isclass(attr) and issubclass(attr, Game) and attr is not Game:
            globals()[attr_name] = attr
            __all__.append(attr_name)

