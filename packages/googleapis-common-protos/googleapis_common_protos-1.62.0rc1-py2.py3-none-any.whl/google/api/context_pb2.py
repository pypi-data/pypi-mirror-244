# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/api/context.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x18google/api/context.proto\x12\ngoogle.api"1\n\x07\x43ontext\x12&\n\x05rules\x18\x01 \x03(\x0b\x32\x17.google.api.ContextRule"\x8d\x01\n\x0b\x43ontextRule\x12\x10\n\x08selector\x18\x01 \x01(\t\x12\x11\n\trequested\x18\x02 \x03(\t\x12\x10\n\x08provided\x18\x03 \x03(\t\x12"\n\x1a\x61llowed_request_extensions\x18\x04 \x03(\t\x12#\n\x1b\x61llowed_response_extensions\x18\x05 \x03(\tBn\n\x0e\x63om.google.apiB\x0c\x43ontextProtoP\x01ZEgoogle.golang.org/genproto/googleapis/api/serviceconfig;serviceconfig\xa2\x02\x04GAPIb\x06proto3'
)


_CONTEXT = DESCRIPTOR.message_types_by_name["Context"]
_CONTEXTRULE = DESCRIPTOR.message_types_by_name["ContextRule"]
Context = _reflection.GeneratedProtocolMessageType(
    "Context",
    (_message.Message,),
    {
        "DESCRIPTOR": _CONTEXT,
        "__module__": "google.api.context_pb2"
        # @@protoc_insertion_point(class_scope:google.api.Context)
    },
)
_sym_db.RegisterMessage(Context)

ContextRule = _reflection.GeneratedProtocolMessageType(
    "ContextRule",
    (_message.Message,),
    {
        "DESCRIPTOR": _CONTEXTRULE,
        "__module__": "google.api.context_pb2"
        # @@protoc_insertion_point(class_scope:google.api.ContextRule)
    },
)
_sym_db.RegisterMessage(ContextRule)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\n\016com.google.apiB\014ContextProtoP\001ZEgoogle.golang.org/genproto/googleapis/api/serviceconfig;serviceconfig\242\002\004GAPI"
    _CONTEXT._serialized_start = 40
    _CONTEXT._serialized_end = 89
    _CONTEXTRULE._serialized_start = 92
    _CONTEXTRULE._serialized_end = 233
# @@protoc_insertion_point(module_scope)
