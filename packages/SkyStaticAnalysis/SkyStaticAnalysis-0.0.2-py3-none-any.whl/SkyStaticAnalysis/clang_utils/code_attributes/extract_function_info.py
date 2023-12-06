from typing import Generator
from clang.cindex import Cursor, CursorKind, TypeKind
from SkyStaticAnalysis.utils import sky_generator, SkyGenerator


@sky_generator
def get_local_var_defs(c: Cursor) -> SkyGenerator[Generator[Cursor, None, None]]:
    """
    Get all local variable definitions from a function
    except variables from parameters
    """
    assert c.kind == CursorKind.FUNCTION_DECL, c
    child: Cursor
    for child in c.walk_preorder():
        match child:
            case Cursor(kind=CursorKind.VAR_DECL):
                yield child


@sky_generator
def get_var_refs(
    c: Cursor, include_funcs=False
) -> SkyGenerator[Generator[Cursor, None, None]]:
    """
    Get all variables referenced from one function body
    """
    assert c.kind == CursorKind.FUNCTION_DECL, c
    child: Cursor
    for child in c.walk_preorder():
        match child:
            case Cursor(kind=CursorKind.DECL_REF_EXPR, type=type):
                match type.kind:
                    case TypeKind.FUNCTIONPROTO if not include_funcs:
                        continue
                    case _:
                        yield child


@sky_generator
def get_param_decls(c: Cursor) -> SkyGenerator[Generator[Cursor, None, None]]:
    """
    Extract parameter declarations from function definition
    """
    assert c.kind == CursorKind.FUNCTION_DECL, c
    child: Cursor
    for child in c.walk_preorder():
        if child.kind == CursorKind.PARM_DECL:
            yield child


@sky_generator
def get_global_ref_names(c: Cursor) -> SkyGenerator[Generator[str, None, None]]:
    """
    Get all global variables referenced in one function
    """
    assert c.kind == CursorKind.FUNCTION_DECL, c
    all_var_refs = get_var_refs(c).attributes("spelling").to_set()
    local_var_defs = get_local_var_defs(c).attributes("spelling").to_set()
    param_var_defs = get_param_decls(c).attributes("spelling").to_set()
    vars = all_var_refs - local_var_defs - param_var_defs
    for v in vars:
        yield v
