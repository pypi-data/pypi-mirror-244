from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Filter(_message.Message):
    __slots__ = ["field", "function", "values"]
    class Function(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CONTAINS: Filter.Function
    EQUAL: Filter.Function
    FIELD_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    GREATER_THAN: Filter.Function
    GREATER_THAN_OR_EQUAL: Filter.Function
    LESS_THAN: Filter.Function
    LESS_THAN_OR_EQUAL: Filter.Function
    NOT_EQUAL: Filter.Function
    VALUES_FIELD_NUMBER: _ClassVar[int]
    VALUE_IN: Filter.Function
    field: str
    function: Filter.Function
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, function: _Optional[_Union[Filter.Function, str]] = ..., field: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...

class ListRequest(_message.Message):
    __slots__ = ["filters", "limit", "raw_filters", "sort_by", "token"]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    RAW_FILTERS_FIELD_NUMBER: _ClassVar[int]
    SORT_BY_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    filters: _containers.RepeatedCompositeFieldContainer[Filter]
    limit: int
    raw_filters: _containers.RepeatedScalarFieldContainer[str]
    sort_by: Sort
    token: str
    def __init__(self, limit: _Optional[int] = ..., token: _Optional[str] = ..., sort_by: _Optional[_Union[Sort, _Mapping]] = ..., filters: _Optional[_Iterable[_Union[Filter, _Mapping]]] = ..., raw_filters: _Optional[_Iterable[str]] = ...) -> None: ...

class Sort(_message.Message):
    __slots__ = ["direction", "key"]
    class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ASCENDING: Sort.Direction
    DESCENDING: Sort.Direction
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    direction: Sort.Direction
    key: str
    def __init__(self, key: _Optional[str] = ..., direction: _Optional[_Union[Sort.Direction, str]] = ...) -> None: ...
