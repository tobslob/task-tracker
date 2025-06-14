import sys
import types
import python_multipart

# Provide clean "multipart" module alias used by Starlette without triggering
# warnings from the legacy shim bundled with python-multipart.
sys.modules.setdefault("multipart", python_multipart)
sys.modules.setdefault("multipart.multipart", python_multipart.multipart)

# Prevent importing the deprecated builtin ``crypt`` module which would emit a
# warning under Python 3.12+. Passlib will gracefully fall back to pure Python
# implementations when the module is missing.
if "crypt" not in sys.modules:
    crypt_stub = types.ModuleType("crypt")
    crypt_stub.crypt = None
    crypt_stub.methods = []
    sys.modules["crypt"] = crypt_stub
