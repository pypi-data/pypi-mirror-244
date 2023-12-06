from common import list_pb2 as _list_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetadataRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MetadataResponse(_message.Message):
    __slots__ = ["max_single_part_object_size_bytes", "min_part_size_bytes", "max_part_size_bytes"]
    MAX_SINGLE_PART_OBJECT_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    MIN_PART_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    MAX_PART_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    max_single_part_object_size_bytes: int
    min_part_size_bytes: int
    max_part_size_bytes: int
    def __init__(self, max_single_part_object_size_bytes: _Optional[int] = ..., min_part_size_bytes: _Optional[int] = ..., max_part_size_bytes: _Optional[int] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ["tag"]
    class TagEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TAG_FIELD_NUMBER: _ClassVar[int]
    tag: _containers.ScalarMap[str, str]
    def __init__(self, tag: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Object(_message.Message):
    __slots__ = ["contents"]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    contents: bytes
    def __init__(self, contents: _Optional[bytes] = ...) -> None: ...

class PutRequest(_message.Message):
    __slots__ = ["key", "metadata", "object"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    key: str
    metadata: Metadata
    object: Object
    def __init__(self, key: _Optional[str] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ..., object: _Optional[_Union[Object, _Mapping]] = ...) -> None: ...

class PutResponse(_message.Message):
    __slots__ = ["size_bytes", "etag"]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    size_bytes: int
    etag: str
    def __init__(self, size_bytes: _Optional[int] = ..., etag: _Optional[str] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ["key"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ["object", "metadata", "size_bytes", "etag"]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    object: Object
    metadata: Metadata
    size_bytes: int
    etag: str
    def __init__(self, object: _Optional[_Union[Object, _Mapping]] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ..., size_bytes: _Optional[int] = ..., etag: _Optional[str] = ...) -> None: ...

class ListRequest(_message.Message):
    __slots__ = ["request"]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _list_pb2.ListRequest
    def __init__(self, request: _Optional[_Union[_list_pb2.ListRequest, _Mapping]] = ...) -> None: ...

class ListResponse(_message.Message):
    __slots__ = ["keys", "next_token"]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    NEXT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    next_token: str
    def __init__(self, keys: _Optional[_Iterable[str]] = ..., next_token: _Optional[str] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ["key"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HeadRequest(_message.Message):
    __slots__ = ["key"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class HeadResponse(_message.Message):
    __slots__ = ["metadata", "etag", "size_bytes"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    metadata: Metadata
    etag: str
    size_bytes: int
    def __init__(self, metadata: _Optional[_Union[Metadata, _Mapping]] = ..., etag: _Optional[str] = ..., size_bytes: _Optional[int] = ...) -> None: ...

class CreateLargeObjectUploadLocationRequest(_message.Message):
    __slots__ = ["key", "size_bytes", "expires_in"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    key: str
    size_bytes: int
    expires_in: _duration_pb2.Duration
    def __init__(self, key: _Optional[str] = ..., size_bytes: _Optional[int] = ..., expires_in: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class httpHeaderValues(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class SignedPartRequest(_message.Message):
    __slots__ = ["part_number", "expires_at", "url", "method", "headers"]
    class HeadersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: httpHeaderValues
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[httpHeaderValues, _Mapping]] = ...) -> None: ...
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    part_number: int
    expires_at: _timestamp_pb2.Timestamp
    url: str
    method: str
    headers: _containers.MessageMap[str, httpHeaderValues]
    def __init__(self, part_number: _Optional[int] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., url: _Optional[str] = ..., method: _Optional[str] = ..., headers: _Optional[_Mapping[str, httpHeaderValues]] = ...) -> None: ...

class SuccessfulUploadRequest(_message.Message):
    __slots__ = ["etags_parts"]
    class EtagsPartsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    ETAGS_PARTS_FIELD_NUMBER: _ClassVar[int]
    etags_parts: _containers.ScalarMap[str, int]
    def __init__(self, etags_parts: _Optional[_Mapping[str, int]] = ...) -> None: ...

class AbortUploadRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TerminateLargeObjectUploadRequest(_message.Message):
    __slots__ = ["operation_id", "key", "successful_upload", "abort_upload"]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    SUCCESSFUL_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    ABORT_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    key: str
    successful_upload: SuccessfulUploadRequest
    abort_upload: AbortUploadRequest
    def __init__(self, operation_id: _Optional[str] = ..., key: _Optional[str] = ..., successful_upload: _Optional[_Union[SuccessfulUploadRequest, _Mapping]] = ..., abort_upload: _Optional[_Union[AbortUploadRequest, _Mapping]] = ...) -> None: ...

class TerminateLargeObjectUploadResponse(_message.Message):
    __slots__ = ["key", "etag"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    key: str
    etag: str
    def __init__(self, key: _Optional[str] = ..., etag: _Optional[str] = ...) -> None: ...

class CreateLargeObjectUploadLocationResponse(_message.Message):
    __slots__ = ["operation_id", "signed_part_requests", "native_url"]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNED_PART_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    NATIVE_URL_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    signed_part_requests: _containers.RepeatedCompositeFieldContainer[SignedPartRequest]
    native_url: str
    def __init__(self, operation_id: _Optional[str] = ..., signed_part_requests: _Optional[_Iterable[_Union[SignedPartRequest, _Mapping]]] = ..., native_url: _Optional[str] = ...) -> None: ...

class CreateLargeObjectDownloadLinkRequest(_message.Message):
    __slots__ = ["key", "expires_in"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    key: str
    expires_in: _duration_pb2.Duration
    def __init__(self, key: _Optional[str] = ..., expires_in: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class CreateLargeObjectDownloadLinkResponse(_message.Message):
    __slots__ = ["signed_url", "expires_at"]
    SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    signed_url: str
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, signed_url: _Optional[str] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class StartLargeObjectUploadRequest(_message.Message):
    __slots__ = ["key", "metadata"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    key: str
    metadata: Metadata
    def __init__(self, key: _Optional[str] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ...) -> None: ...

class StartLargeObjectUploadResponse(_message.Message):
    __slots__ = ["operation_id", "expires_at"]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, operation_id: _Optional[str] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UploadPartRequest(_message.Message):
    __slots__ = ["operation_id", "key", "part_number", "object", "content_length"]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_LENGTH_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    key: str
    part_number: int
    object: Object
    content_length: int
    def __init__(self, operation_id: _Optional[str] = ..., key: _Optional[str] = ..., part_number: _Optional[int] = ..., object: _Optional[_Union[Object, _Mapping]] = ..., content_length: _Optional[int] = ...) -> None: ...

class UploadPartResponse(_message.Message):
    __slots__ = ["etag"]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    etag: str
    def __init__(self, etag: _Optional[str] = ...) -> None: ...

class ListInProgressLargeObjectUploadsRequest(_message.Message):
    __slots__ = ["request"]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _list_pb2.ListRequest
    def __init__(self, request: _Optional[_Union[_list_pb2.ListRequest, _Mapping]] = ...) -> None: ...

class LargeObjectUpload(_message.Message):
    __slots__ = ["operation_id", "key"]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    key: str
    def __init__(self, operation_id: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class ListInProgressLargeObjectUploadsResponse(_message.Message):
    __slots__ = ["operations"]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    operations: _containers.RepeatedCompositeFieldContainer[LargeObjectUpload]
    def __init__(self, operations: _Optional[_Iterable[_Union[LargeObjectUpload, _Mapping]]] = ...) -> None: ...

class DownloadPartRequest(_message.Message):
    __slots__ = ["key", "start_pos", "size_bytes"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    START_POS_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    key: str
    start_pos: int
    size_bytes: int
    def __init__(self, key: _Optional[str] = ..., start_pos: _Optional[int] = ..., size_bytes: _Optional[int] = ...) -> None: ...

class DownloadPartResponse(_message.Message):
    __slots__ = ["object"]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    object: Object
    def __init__(self, object: _Optional[_Union[Object, _Mapping]] = ...) -> None: ...

class CopyRequest(_message.Message):
    __slots__ = ["source_key", "destination_key"]
    SOURCE_KEY_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_KEY_FIELD_NUMBER: _ClassVar[int]
    source_key: str
    destination_key: str
    def __init__(self, source_key: _Optional[str] = ..., destination_key: _Optional[str] = ...) -> None: ...

class CopyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
