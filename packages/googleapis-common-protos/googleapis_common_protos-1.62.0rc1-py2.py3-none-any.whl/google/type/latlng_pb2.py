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
# source: google/type/latlng.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x18google/type/latlng.proto\x12\x0bgoogle.type"-\n\x06LatLng\x12\x10\n\x08latitude\x18\x01 \x01(\x01\x12\x11\n\tlongitude\x18\x02 \x01(\x01\x42\x63\n\x0f\x63om.google.typeB\x0bLatLngProtoP\x01Z8google.golang.org/genproto/googleapis/type/latlng;latlng\xf8\x01\x01\xa2\x02\x03GTPb\x06proto3'
)


_LATLNG = DESCRIPTOR.message_types_by_name["LatLng"]
LatLng = _reflection.GeneratedProtocolMessageType(
    "LatLng",
    (_message.Message,),
    {
        "DESCRIPTOR": _LATLNG,
        "__module__": "google.type.latlng_pb2"
        # @@protoc_insertion_point(class_scope:google.type.LatLng)
    },
)
_sym_db.RegisterMessage(LatLng)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\n\017com.google.typeB\013LatLngProtoP\001Z8google.golang.org/genproto/googleapis/type/latlng;latlng\370\001\001\242\002\003GTP"
    _LATLNG._serialized_start = 41
    _LATLNG._serialized_end = 86
# @@protoc_insertion_point(module_scope)
