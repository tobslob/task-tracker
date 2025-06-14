
"""Initialization for the ``app`` package.

This module applies a couple of compatibility patches before the rest of the
project imports third party libraries.  These patches ensure newer Python
versions don't emit deprecation warnings for deprecated modules used by some
dependencies.
"""

from __future__ import annotations

import sys
import types

try:  # python-multipart exposes the 'multipart' package only
    import python_multipart
except ModuleNotFoundError:  # fallback for python-multipart>=0.0.9
    import multipart as python_multipart

# ---------------------------------------------------------------------------
# Avoid ``PendingDeprecationWarning`` triggered by Starlette importing the
# ``multipart`` package.  The ``python-multipart`` distribution installs a
# legacy ``multipart`` module which emits this warning on import.  By adding a
# module alias here, Starlette resolves ``multipart`` without importing the
# deprecated shim and therefore no warning is issued.
# ---------------------------------------------------------------------------
sys.modules.setdefault("multipart", python_multipart)
sys.modules.setdefault("multipart.multipart", python_multipart.multipart)


# ---------------------------------------------------------------------------
# Avoid ``DeprecationWarning`` raised when importing Python's built in ``crypt``
# module.  Passlib tries to import ``crypt`` to provide access to system level
# hashing algorithms.  The module is deprecated in Python 3.12+ which results in
# a warning during import.  Providing a minimal stub in ``sys.modules`` prevents
# the deprecated module from being loaded at all.  Passlib will fall back to its
# pure Python implementations instead.
# ---------------------------------------------------------------------------
if "crypt" not in sys.modules:  # pragma: no cover - executed at import time
    crypt_stub = types.ModuleType("crypt")
    crypt_stub.crypt = None  # signal that system crypt is unavailable
    crypt_stub.methods = []
    sys.modules["crypt"] = crypt_stub
