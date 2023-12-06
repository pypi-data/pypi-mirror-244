from typing import Callable, Generator, Generic, List, TypeVar

VARTYPE = TypeVar("VARTYPE")


class SkyGenerator(Generic[VARTYPE]):
    def __init__(self, inner: Generator):
        self.inner = inner

    def __iter__(self):
        return self

    def __next__(self) -> VARTYPE:
        return self.inner.__next__()

    def attributes(self, attr: str):
        """
        Get attribute from each remaining items
        """

        def _(orig_gen):
            item: VARTYPE
            for item in orig_gen:
                yield getattr(item, attr)

        return SkyGenerator(_(self.inner))

    def to_list(self) -> List[VARTYPE]:
        return list(self.inner)

    def to_set(self) -> List[VARTYPE]:
        return set(self.inner)


def sky_generator(f: VARTYPE):
    def inner(*args, **kwargs):
        return SkyGenerator(f(*args, **kwargs))

    return inner


def generator_next(g: Generator[VARTYPE, None, None]) -> tuple[VARTYPE, bool]:
    try:
        return next(g), True
    except StopIteration:
        return None, False
