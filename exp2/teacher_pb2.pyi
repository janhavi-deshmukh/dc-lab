from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TeacherData(_message.Message):
    __slots__ = ("name", "phone_no", "password")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_NO_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    name: str
    phone_no: str
    password: str
    def __init__(self, name: _Optional[str] = ..., phone_no: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class Teachers(_message.Message):
    __slots__ = ("data",)
    class TeacherData(_message.Message):
        __slots__ = ("name", "phone_no", "id")
        NAME_FIELD_NUMBER: _ClassVar[int]
        PHONE_NO_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        name: str
        phone_no: str
        id: int
        def __init__(self, name: _Optional[str] = ..., phone_no: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[Teachers.TeacherData]
    def __init__(self, data: _Optional[_Iterable[_Union[Teachers.TeacherData, _Mapping]]] = ...) -> None: ...

class Temp(_message.Message):
    __slots__ = ("field",)
    FIELD_FIELD_NUMBER: _ClassVar[int]
    field: str
    def __init__(self, field: _Optional[str] = ...) -> None: ...
