import os
import clang.native as native
import clang.cindex as cindex


def find_clang_dll():
    path = os.path.join(os.path.dirname(native.__file__))
    filename = list(
        filter(lambda x: x.endswith(("dll", "pyd", "so")), os.listdir(path))
    )[0]
    cindex.Config.set_library_file(os.path.join(path, filename))

find_clang_dll()
if not hasattr(cindex.CursorKind, "BUILTIN_BITCAST_EXPR"):
    cindex.CursorKind.BUILTIN_BITCAST_EXPR = cindex.CursorKind(280)


from .code_attributes import *
