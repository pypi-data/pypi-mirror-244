import enum
import json
import os
import sys
from typing import Callable, Dict, List, Optional, Generator, Tuple, Union
from clang import cindex


def parse_file(file: str, args: List = None) -> cindex.TranslationUnit:
    """
    Open a c/cpp file, and return the corresponding translation unit
    """
    if not os.path.exists(file):
        raise FileNotFoundError(file)
    index = cindex.Index.create()

    # open C sourcefile
    if args == "":
        return index.parse(file)
    else:
        return index.parse(file, args=args)


def get_func_decl(node: cindex.Cursor, func_name: str) -> Optional[cindex.Cursor]:
    """
    Get the function named `func_name` from Clang AST. If not exist, return None.
    """
    for node in node.get_children():
        if node.kind == cindex.CursorKind.FUNCTION_DECL:
            if node.spelling == func_name:
                return node
            else:
                continue
    return None


def get_func_decl_all(
    node: cindex.Cursor, definition_only=False
) -> List[cindex.Cursor]:
    """
    Get all function definitions from Clang AST.

    :definition_only: False by default. If true, this function will return functions with definitions
     only. Otherwise, this function will return both defined and declared functions
    """
    func_decls = []
    for node in node.get_children():
        if node.kind == cindex.CursorKind.FUNCTION_DECL:
            if not definition_only or (definition_only and node.is_definition()):
                func_decls.append(node)
    return func_decls


class TraversalContext:
    """
    Used when traversing the Clang AST with recording the AST hierarchy information.
    """

    def __init__(self) -> None:
        self.hierarchy: List[cindex.Cursor] = []

    def print_hierarchy(self):
        print([c.kind for c in self.hierarchy])

    @property
    def current_node(self) -> cindex.Cursor:
        """
        Current node in the Clang AST
        """
        if len(self.hierarchy) > 0:
            return self.hierarchy[-1]
        else:
            raise ValueError("Traversal context does not contain any node.")

    def _push(self, node: cindex.Cursor):
        self.hierarchy.append(node)

    def _pop(self):
        self.hierarchy.pop()

    def find_by_kind(self, kind: cindex.CursorKind):
        """
        Search the AST hierarchy, get the AST node of the same kind.
        """
        for item in self.hierarchy:
            if item.kind == kind:
                return item
        return None

    def find_by_kind_td(self, kind: cindex.CursorKind):
        """
        Perform top-down search by AST node kind in the hierarchy.
        """
        for item in reversed(self.hierarchy):
            if item.kind == kind:
                return item
        return None

    def nearest_statement(self) -> Tuple[cindex.Cursor, cindex.Cursor]:
        """
        Find nearest Compound Statement

        :return:
        """
        compound_stmt: cindex.Cursor = None
        index = len(self.hierarchy)
        for item in reversed(self.hierarchy):
            index -= 1
            if item.kind in {cindex.CursorKind.COMPOUND_STMT}:
                compound_stmt = item
                break

        expr: cindex.Cursor = self.hierarchy[index + 1]  # compound_stmt下的
        return compound_stmt, expr

    def __len__(self):
        return len(self.hierarchy)


TraversalCallbackType = Callable[[TraversalContext], None]


def _traversal(
    node: cindex.Cursor, ctx: TraversalContext, func: TraversalCallbackType
) -> List[cindex.Cursor]:
    for subnode in node.get_children():
        ctx._push(subnode)
        func(ctx)
        _traversal(subnode, ctx, func)
        ctx._pop()
    return


def split_binary_operator(
    node: cindex.Cursor,
) -> Tuple[cindex.Cursor, str, cindex.Cursor]:
    """
    Split binary operator.

    .. code-block:: python

        left, op, right = split_binary_operator(cursor)

    The result:
        * left: a Cursor object
        * right: a Cursor object
        * op:  a str, "+"

    """
    assert node.kind == cindex.CursorKind.BINARY_OPERATOR, node.kind
    children_iterator = node.get_children()
    left = next(children_iterator)
    symbol = list(node.get_tokens())[len(list(left.get_tokens()))].spelling
    right = next(children_iterator)
    return left, symbol, right


class UnaryOpPos(enum.Enum):
    """
    A Enum standing for the positional relationship of unary operator
    and its target expression
    
    * BEFORE: Operator is before the expression, such as ``*p``, ``++i``
    * AFTER: Operator is after the expression, such as ``p++``
    """


    BEFORE = "before"
    AFTER = "after"


def split_unary_operator(
    node: cindex.Cursor,
) -> Tuple[str, cindex.Cursor, UnaryOpPos]:
    """
    Split unary operator

    :return: A tuple, (Unary Operator, operated expression, operator is before/after expression)
    """
    assert node.kind == cindex.CursorKind.UNARY_OPERATOR, node.kind
    node_tokens = "".join([t.spelling for t in node.get_tokens()])
    child = next(node.get_children())
    child_tokens = "".join([t.spelling for t in child.get_tokens()])
    if node_tokens.startswith(child_tokens):  # unary operator is after child expression
        return node_tokens[len(child_tokens) :], child, UnaryOpPos.AFTER
    else:
        return node_tokens[: -len(child_tokens)], child, UnaryOpPos.BEFORE


def get_compound_assignment_operator(node: cindex.Cursor) -> str:
    """
    get the symbol of COMPOUND_ASSIGNMENT_OPERATOR
    """
    assert node.kind == cindex.CursorKind.COMPOUND_ASSIGNMENT_OPERATOR, node.kind

    left = next(node.get_children())
    symbol = list(node.get_tokens())[len(list(left.get_tokens()))].spelling
    return symbol


def traversal(node: cindex.Cursor, func: TraversalCallbackType):
    """
    Traverse the AST and for each node call `func`
    """
    ctx = TraversalContext()
    ctx._push(node)
    func(ctx)
    _traversal(node, ctx, func)
    ctx._pop()


def iterate_files(
    folder: str,
    filetypes: Union[str, Tuple[str], Callable[[str], bool]] = "",
    abspath=True,
) -> Generator[str, None, None]:
    """
    Iterate all files inside the folder.
    """
    if not callable(filetypes):
        if filetypes != "":

            def filter_func(s: str):
                return s.endswith(filetypes)

        else:

            def filter_func(s):
                return True

    else:
        filter_func = filetypes
    for root, _, files in os.walk(folder):
        for file in files:
            if filter_func(file):
                yield os.path.join(root, file) if abspath else file


def is_literal_kind(node: cindex.Cursor):
    return node.kind in {
        cindex.CursorKind.INTEGER_LITERAL,
        cindex.CursorKind.FLOATING_LITERAL,
        cindex.CursorKind.IMAGINARY_LITERAL,
        cindex.CursorKind.STRING_LITERAL,
        cindex.CursorKind.CHARACTER_LITERAL,
    }


def extract_literal_value(node: cindex.Cursor):
    assert is_literal_kind(node)
    tokens = list(node.get_tokens())
    if len(tokens) >= 1:
        return tokens[0].spelling
    else:
        return None


class ASTExtractor:
    def __init__(self):
        self.node_inc_id = 0

    def _ast_extract(self, node: cindex.Cursor, ast_struct: Dict):
        ast_struct["id"] = self.node_inc_id
        has_kind = False
        # try:
        ast_struct["kind"] = node.kind.value
        ast_struct["kindText"] = str(node.kind)
        has_kind = True
        ast_struct["position"] = (node.location.line, node.location.column)

        try:
            node_type: cindex.Type = node.type
            ast_struct["type"] = {
                "spelling": node_type.spelling,
                "kind": str(node_type.kind),
            }
            if node_type.kind == cindex.TypeKind.POINTER:
                pointee_type: cindex.Type = node_type.get_pointee()
                ast_struct["type"]["pointee"] = str(pointee_type.spelling)
        except:
            import traceback

            traceback.print_exc()
            pass
        self.node_inc_id += 1

        # node may not be Cursor, but must have property `kind`, and method `get_children`
        if isinstance(node, cindex.Cursor):
            if node.spelling:
                ast_struct["spelling"] = node.spelling
            elif has_kind and is_literal_kind(node):
                # tokens = list(node.get_tokens())
                # if len(tokens) >= 1:
                # assert len(tokens) == 1, [t.spelling for t in tokens]
                # value = tokens[0].spelling
                # if node.kind == cindex.CursorKind.INTEGER_LITERAL:
                #     value = value
                # elif node.kind == cindex.CursorKind.FLOATING_LITERAL:
                #     value = value
                ast_struct["value"] = extract_literal_value(node)

        subnode: cindex.Cursor
        for subnode in node.get_children():
            if "children" not in ast_struct:
                ast_struct["children"] = []
            props = {}
            self._ast_extract(subnode, props)
            ast_struct["children"].append(props)

    def extract(self, node: cindex.Cursor):
        ast_root = {}
        self._ast_extract(node, ast_root)
        return ast_root


def extract_ast(node: cindex.Cursor):
    """
    Convert a Clang-AST node to a JSON
    """
    return ASTExtractor().extract(node)


def beautified_print_ast(node: cindex.Cursor, filename=""):
    """
    Print Clang-AST with indented-JSON format
    
    :param filename: 
        
        * If ``""``, print to stdout; 
        * If provided a valid filename, write the JSON to the file.
    """
    if filename == "":
        file = sys.stdout
        print(json.dumps(extract_ast(node), indent=2), file=file)
    else:
        with open(filename, "w") as file:
            print(json.dumps(extract_ast(node), indent=2), file=file)


# def get_file_and_line(node: cindex.Cursor)->Tuple[str, int, int]:
#     # 获取源代码位置
#     location: cindex.SourceLocation = node.location

#     print(location)
#     # 获取文件名
#     file_name = cindex.conf.get_filename(location)

#     # 获取行号和列号
#     line = location.line
#     column = location.column

#     return file_name, line, column
