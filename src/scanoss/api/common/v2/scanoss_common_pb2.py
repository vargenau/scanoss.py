# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scanoss/api/common/v2/scanoss-common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='scanoss/api/common/v2/scanoss-common.proto',
  package='scanoss.api.common.v2',
  syntax='proto3',
  serialized_options=b'Z-github.com/scanoss/papi/api/commonv2;commonv2',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n*scanoss/api/common/v2/scanoss-common.proto\x12\x15scanoss.api.common.v2\"L\n\x06Status\x12\x31\n\x06status\x18\x01 \x01(\x0e\x32!.scanoss.api.common.v2.StatusCode\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x1e\n\x0b\x45\x63hoRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1f\n\x0c\x45\x63hoResponse\x12\x0f\n\x07message\x18\x01 \x01(\t*C\n\nStatusCode\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\x0b\n\x07WARNING\x10\x02\x12\n\n\x06\x46\x41ILED\x10\x03\x42/Z-github.com/scanoss/papi/api/commonv2;commonv2b\x06proto3'
)

_STATUSCODE = _descriptor.EnumDescriptor(
  name='StatusCode',
  full_name='scanoss.api.common.v2.StatusCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WARNING', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FAILED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=212,
  serialized_end=279,
)
_sym_db.RegisterEnumDescriptor(_STATUSCODE)

StatusCode = enum_type_wrapper.EnumTypeWrapper(_STATUSCODE)
UNSPECIFIED = 0
SUCCESS = 1
WARNING = 2
FAILED = 3



_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='scanoss.api.common.v2.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='scanoss.api.common.v2.Status.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='scanoss.api.common.v2.Status.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=145,
)


_ECHOREQUEST = _descriptor.Descriptor(
  name='EchoRequest',
  full_name='scanoss.api.common.v2.EchoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='scanoss.api.common.v2.EchoRequest.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=147,
  serialized_end=177,
)


_ECHORESPONSE = _descriptor.Descriptor(
  name='EchoResponse',
  full_name='scanoss.api.common.v2.EchoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='scanoss.api.common.v2.EchoResponse.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=179,
  serialized_end=210,
)

_STATUS.fields_by_name['status'].enum_type = _STATUSCODE
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
DESCRIPTOR.message_types_by_name['EchoRequest'] = _ECHOREQUEST
DESCRIPTOR.message_types_by_name['EchoResponse'] = _ECHORESPONSE
DESCRIPTOR.enum_types_by_name['StatusCode'] = _STATUSCODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'scanoss.api.common.v2.scanoss_common_pb2'
  # @@protoc_insertion_point(class_scope:scanoss.api.common.v2.Status)
  })
_sym_db.RegisterMessage(Status)

EchoRequest = _reflection.GeneratedProtocolMessageType('EchoRequest', (_message.Message,), {
  'DESCRIPTOR' : _ECHOREQUEST,
  '__module__' : 'scanoss.api.common.v2.scanoss_common_pb2'
  # @@protoc_insertion_point(class_scope:scanoss.api.common.v2.EchoRequest)
  })
_sym_db.RegisterMessage(EchoRequest)

EchoResponse = _reflection.GeneratedProtocolMessageType('EchoResponse', (_message.Message,), {
  'DESCRIPTOR' : _ECHORESPONSE,
  '__module__' : 'scanoss.api.common.v2.scanoss_common_pb2'
  # @@protoc_insertion_point(class_scope:scanoss.api.common.v2.EchoResponse)
  })
_sym_db.RegisterMessage(EchoResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
