from typing import Generator, Iterable, Optional, Union
from clang.cindex import Cursor, CursorKind, TypeKind
from SkyStaticAnalysis.utils import generator_next
from .utils import split_binary_operator, split_unary_operator


def format_result(result: Iterable[Optional[Cursor]]):
    if result is None:
        return None
    if isinstance(result, Cursor):
        return f"{str(result.kind).split('.')[1]}:{result.spelling}"
    return [
        f"{str(item.kind).split('.')[1]}:{item.spelling}"
        if isinstance(item, Cursor)
        else item
        for item in result
    ]


class CProgramWalker:
    LOG_VISITED_NODES = True

    def cursor_parser_decorator(func):
        def wrapper(self: "CProgramWalker", *args, **kw):
            # print visited functions with indentation
            indentation = "  " * self.recurse_count
            if CProgramWalker.LOG_VISITED_NODES:
                print(indentation + f"<{func.__name__}>")
            self.recurse_count += 1
            result = func(self, *args, **kw)
            self.recurse_count -= 1
            if CProgramWalker.LOG_VISITED_NODES:
                print(indentation + "  " + f"<result>{format_result(result)}<result/>")
                print(indentation + f"<{func.__name__}/>")
            return result

        return wrapper

    def __init__(self) -> None:
        self.recurse_count = 0

    def parse_statement(self, c: Cursor):
        self.parse_statement_children(c.get_children())

    def parse_statement_children(self, children: Generator[Cursor, None, None]):
        first, stat = generator_next(children)
        if stat:
            self.parse_single_statement(first)
            self.parse_statement_children(children)

    def parse_single_statement(self, c: Cursor):
        match c.kind:
            case CursorKind.CALL_EXPR:
                ret = self.parse_call_expr(c)

            case CursorKind.ARRAY_SUBSCRIPT_EXPR:
                ret = self.parse_array_subscript_expr(c)

            case CursorKind.DECL_REF_EXPR:
                ret = self.parse_decl_ref_expr(c)

            case CursorKind.BINARY_OPERATOR:
                ret = self.parse_binary_operator(c)

            case CursorKind.CSTYLE_CAST_EXPR:
                ret = self.parse_c_style_cast_expr(c)

            case CursorKind.VAR_DECL:
                ret = self.parse_var_decl(c)

            case CursorKind.IF_STMT:
                ret = self.parse_statement_children(c.get_children())

            case CursorKind.UNEXPOSED_EXPR | CursorKind.DECL_STMT | CursorKind.COMPOUND_STMT:
                ret = self.parse_statement_children(c.get_children())

            case _:
                raise NotImplementedError(c.kind)
        return ret

    @cursor_parser_decorator
    def parse_call_expr(self, c: Cursor):
        children: Generator[Cursor, None, None] = c.get_children()
        target_fcn, args = next(children), children
        # print("target_fcn", target_fcn.spelling)
        self.parse_statement_children(args)
        pass

    @cursor_parser_decorator
    def parse_array_subscript_expr(self, c: Cursor):
        children: Generator[Cursor, None, None] = c.get_children()
        target_arr, *args = children
        assert len(args) == 1
        self.parse_single_statement(args[0])
        return target_arr, args[0]

    @cursor_parser_decorator
    def parse_decl_ref_expr(self, c: Cursor):
        print("decl_ref expr", c.spelling)
        return c

    @cursor_parser_decorator
    def parse_var_decl(self, c: Cursor):
        # print("decl stmt:", c.spelling)
        pass

    @cursor_parser_decorator
    def parse_binary_operator(self, c: Cursor):
        left, op, right = split_binary_operator(c)
        return left, op, right

    @cursor_parser_decorator
    def parse_c_style_cast_expr(self, c: Cursor):
        pass
