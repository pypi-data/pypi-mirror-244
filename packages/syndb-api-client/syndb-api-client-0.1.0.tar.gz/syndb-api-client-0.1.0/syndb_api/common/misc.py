from typing import Iterable

from sqlalchemy import ScalarResult


def unpack_nested_tuples(nested_tuple: Iterable[tuple]) -> list:
    return [q[0] for q in nested_tuple] if nested_tuple else []


def scalars_all(result: ScalarResult):
    return result.all()
