# Copyright © 2023 Pathway

from __future__ import annotations

import json as _json  # otherwise its easy to mistake `json` and `Json`
from dataclasses import dataclass
from functools import cached_property
from typing import Any, ClassVar


class _JsonEncoder(_json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Json):
            return obj.value
        return super().default(obj)


@dataclass(frozen=True, eq=True)
class Json:
    """Represents JSON values.

    Example:

    >>> import pathway as pw
    >>> t1 = pw.debug.table_from_markdown('''
    ... a    | b | c
    ... True | 2 | manul
    ... ''')
    >>> @pw.udf
    ... def to_json(val) -> pw.Json:
    ...     return pw.Json(val)
    >>> result = t1.select(**{c: to_json(pw.this[c]) for c in t1.column_names()})
    >>> pw.debug.compute_and_print(result, include_id=False)
    a    | b | c
    true | 2 | "manul"
    """

    NULL: ClassVar[Json]

    _value: JsonValue

    def __str__(self) -> str:
        return _json.dumps(self.value)

    def __repr__(self) -> str:
        return f"pw.Json({self.value!r})"

    @cached_property
    def value(self) -> JsonValue:
        if isinstance(self._value, Json):
            return self._value.value
        else:
            return self._value

    @staticmethod
    def parse(value: str | bytes | bytearray) -> Json:
        return Json(_json.loads(value))

    @staticmethod
    def dumps(obj: Any) -> str:
        return _json.dumps(obj, cls=_JsonEncoder)


JsonValue = (
    int | float | str | bool | list["JsonValue"] | dict[str, "JsonValue"] | None | Json
)


Json.NULL = Json(None)

__all__ = ["Json", "JsonValue"]
