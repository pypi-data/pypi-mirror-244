# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trip_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12trip_service.proto\x12\x14mobilegateway.protos\"=\n\x08Waypoint\x12\x10\n\x08latitude\x18\x01 \x01(\x01\x12\x11\n\tlongitude\x18\x02 \x01(\x01\x12\x0c\n\x04name\x18\x03 \x01(\t\"C\n\x04Trip\x12\x0c\n\x04name\x18\x02 \x01(\t\x12-\n\x05route\x18\x07 \x03(\x0b\x32\x1e.mobilegateway.protos.Waypoint\"P\n\x10ShareTripRequest\x12(\n\x04trip\x18\x02 \x01(\x0b\x32\x1a.mobilegateway.protos.Trip\x12\x12\n\nvehicle_id\x18\x03 \x01(\t\"\x13\n\x11ShareTripResponse2m\n\x0bTripService\x12^\n\tShareTrip\x12&.mobilegateway.protos.ShareTripRequest\x1a\'.mobilegateway.protos.ShareTripResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'trip_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_WAYPOINT']._serialized_start=44
  _globals['_WAYPOINT']._serialized_end=105
  _globals['_TRIP']._serialized_start=107
  _globals['_TRIP']._serialized_end=174
  _globals['_SHARETRIPREQUEST']._serialized_start=176
  _globals['_SHARETRIPREQUEST']._serialized_end=256
  _globals['_SHARETRIPRESPONSE']._serialized_start=258
  _globals['_SHARETRIPRESPONSE']._serialized_end=277
  _globals['_TRIPSERVICE']._serialized_start=279
  _globals['_TRIPSERVICE']._serialized_end=388
# @@protoc_insertion_point(module_scope)
