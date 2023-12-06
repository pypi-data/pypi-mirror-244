from typing import Generator
from clang.cindex import Cursor, CursorKind


def all_globals(c: Cursor) -> Generator[Cursor, None, None]:
    assert c.kind == CursorKind.TRANSLATION_UNIT
    child: Cursor
    for child in c.get_children():
        match child:
            case Cursor(kind=CursorKind.VAR_DECL):
                yield child
