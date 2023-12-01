# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: login_session.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import user_profile_service_pb2 as user__profile__service__pb2
import vehicle_state_service_pb2 as vehicle__state__service__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13login_session.proto\x12\x14mobilegateway.protos\x1a\x1auser_profile_service.proto\x1a\x1bvehicle_state_service.proto\"\xad\x02\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12P\n\x19notification_channel_type\x18\x03 \x01(\x0e\x32-.mobilegateway.protos.NotificationChannelType\x12$\n\x02os\x18\x04 \x01(\x0e\x32\x18.mobilegateway.protos.Os\x12!\n\x19notification_device_token\x18\x05 \x01(\t\x12\x0e\n\x06locale\x18\x06 \x01(\t\x12\x16\n\tdevice_id\x18\x07 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x0b\x63lient_name\x18\x08 \x01(\tH\x01\x88\x01\x01\x42\x0c\n\n_device_idB\x0e\n\x0c_client_name\"y\n\x0bSessionInfo\x12\x10\n\x08id_token\x18\x01 \x01(\t\x12\x17\n\x0f\x65xpiry_time_sec\x18\x02 \x01(\x05\x12\x1a\n\rrefresh_token\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x11\n\tgigya_jwt\x18\x04 \x01(\tB\x10\n\x0e_refresh_token\"\xb9\x02\n\rLoginResponse\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x37\n\x0csession_info\x18\x02 \x01(\x0b\x32!.mobilegateway.protos.SessionInfo\x12\x37\n\x0cuser_profile\x18\x03 \x01(\x0b\x32!.mobilegateway.protos.UserProfile\x12\x38\n\x11user_vehicle_data\x18\x04 \x03(\x0b\x32\x1d.mobilegateway.protos.Vehicle\x12\x39\n\rsubscriptions\x18\x05 \x03(\x0e\x32\".mobilegateway.protos.Subscription\x12\x34\n\nencryption\x18\x06 \x01(\x0e\x32 .mobilegateway.protos.Encryption\".\n\x15GetNewJWTTokenRequest\x12\x15\n\rrefresh_token\x18\x01 \x01(\t\"Q\n\x16GetNewJWTTokenResponse\x12\x37\n\x0csession_info\x18\x01 \x01(\x0b\x32!.mobilegateway.protos.SessionInfo\"\x18\n\x16\x43onfirmResetPinRequest\"\x19\n\x17\x43onfirmResetPinResponse\"\x18\n\x16GetSubscriptionRequest\"\x19\n\x17GetSubscriptionResponse\"\x18\n\x16GetUserVehiclesRequest\"\x19\n\x17GetUserVehiclesResponse\"\x0f\n\rLogoutRequest\"\x10\n\x0eLogoutResponse\"!\n\x1fRefreshNotificationTokenRequest\"\"\n RefreshNotificationTokenResponse\"\x14\n\x12SetNickNameRequest\"\x15\n\x13SetNickNameResponse\"\x18\n\x16SetSubscriptionRequest\"\x19\n\x17SetSubscriptionResponse*w\n\x17NotificationChannelType\x12 \n\x1cNOTIFICATION_CHANNEL_UNKNOWN\x10\x00\x12\x1c\n\x18NOTIFICATION_CHANNEL_ONE\x10\x01\x12\x1c\n\x18NOTIFICATION_CHANNEL_TWO\x10\x02*0\n\x02Os\x12\x0e\n\nOS_UNKNOWN\x10\x00\x12\n\n\x06OS_IOS\x10\x01\x12\x0e\n\nOS_ANDROID\x10\x02*\xe4\x01\n\x0cSubscription\x12\x18\n\x14SUBSCRIPTION_UNKNOWN\x10\x00\x12\x17\n\x13SUBSCRIPTION_CHARGE\x10\x01\x12\x19\n\x15SUBSCRIPTION_SECURITY\x10\x02\x12\x19\n\x15SUBSCRIPTION_SOFTWARE\x10\x03\x12\x15\n\x11SUBSCRIPTION_HVAC\x10\x04\x12\x19\n\x15SUBSCRIPTION_REQUIRED\x10\x05\x12\x1a\n\x16SUBSCRIPTION_CDR_EMAIL\x10\x06\x12\x1d\n\x19SUBSCRIPTION_SUBSCRIPTION\x10\x07*;\n\nEncryption\x12\x16\n\x12\x45NCRYPTION_UNKNOWN\x10\x00\x12\x15\n\x11\x45NCRYPTION_SINGLE\x10\x01\x32\xe4\x07\n\x0cLoginSession\x12p\n\x0f\x43onfirmResetPin\x12,.mobilegateway.protos.ConfirmResetPinRequest\x1a-.mobilegateway.protos.ConfirmResetPinResponse\"\x00\x12m\n\x0eGetNewJWTToken\x12+.mobilegateway.protos.GetNewJWTTokenRequest\x1a,.mobilegateway.protos.GetNewJWTTokenResponse\"\x00\x12p\n\x0fGetSubscription\x12,.mobilegateway.protos.GetSubscriptionRequest\x1a-.mobilegateway.protos.GetSubscriptionResponse\"\x00\x12p\n\x0fGetUserVehicles\x12,.mobilegateway.protos.GetUserVehiclesRequest\x1a-.mobilegateway.protos.GetUserVehiclesResponse\"\x00\x12R\n\x05Login\x12\".mobilegateway.protos.LoginRequest\x1a#.mobilegateway.protos.LoginResponse\"\x00\x12U\n\x06Logout\x12#.mobilegateway.protos.LogoutRequest\x1a$.mobilegateway.protos.LogoutResponse\"\x00\x12\x8b\x01\n\x18RefreshNotificationToken\x12\x35.mobilegateway.protos.RefreshNotificationTokenRequest\x1a\x36.mobilegateway.protos.RefreshNotificationTokenResponse\"\x00\x12\x64\n\x0bSetNickName\x12(.mobilegateway.protos.SetNickNameRequest\x1a).mobilegateway.protos.SetNickNameResponse\"\x00\x12p\n\x0fSetSubscription\x12,.mobilegateway.protos.SetSubscriptionRequest\x1a-.mobilegateway.protos.SetSubscriptionResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'login_session_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_NOTIFICATIONCHANNELTYPE']._serialized_start=1339
  _globals['_NOTIFICATIONCHANNELTYPE']._serialized_end=1458
  _globals['_OS']._serialized_start=1460
  _globals['_OS']._serialized_end=1508
  _globals['_SUBSCRIPTION']._serialized_start=1511
  _globals['_SUBSCRIPTION']._serialized_end=1739
  _globals['_ENCRYPTION']._serialized_start=1741
  _globals['_ENCRYPTION']._serialized_end=1800
  _globals['_LOGINREQUEST']._serialized_start=103
  _globals['_LOGINREQUEST']._serialized_end=404
  _globals['_SESSIONINFO']._serialized_start=406
  _globals['_SESSIONINFO']._serialized_end=527
  _globals['_LOGINRESPONSE']._serialized_start=530
  _globals['_LOGINRESPONSE']._serialized_end=843
  _globals['_GETNEWJWTTOKENREQUEST']._serialized_start=845
  _globals['_GETNEWJWTTOKENREQUEST']._serialized_end=891
  _globals['_GETNEWJWTTOKENRESPONSE']._serialized_start=893
  _globals['_GETNEWJWTTOKENRESPONSE']._serialized_end=974
  _globals['_CONFIRMRESETPINREQUEST']._serialized_start=976
  _globals['_CONFIRMRESETPINREQUEST']._serialized_end=1000
  _globals['_CONFIRMRESETPINRESPONSE']._serialized_start=1002
  _globals['_CONFIRMRESETPINRESPONSE']._serialized_end=1027
  _globals['_GETSUBSCRIPTIONREQUEST']._serialized_start=1029
  _globals['_GETSUBSCRIPTIONREQUEST']._serialized_end=1053
  _globals['_GETSUBSCRIPTIONRESPONSE']._serialized_start=1055
  _globals['_GETSUBSCRIPTIONRESPONSE']._serialized_end=1080
  _globals['_GETUSERVEHICLESREQUEST']._serialized_start=1082
  _globals['_GETUSERVEHICLESREQUEST']._serialized_end=1106
  _globals['_GETUSERVEHICLESRESPONSE']._serialized_start=1108
  _globals['_GETUSERVEHICLESRESPONSE']._serialized_end=1133
  _globals['_LOGOUTREQUEST']._serialized_start=1135
  _globals['_LOGOUTREQUEST']._serialized_end=1150
  _globals['_LOGOUTRESPONSE']._serialized_start=1152
  _globals['_LOGOUTRESPONSE']._serialized_end=1168
  _globals['_REFRESHNOTIFICATIONTOKENREQUEST']._serialized_start=1170
  _globals['_REFRESHNOTIFICATIONTOKENREQUEST']._serialized_end=1203
  _globals['_REFRESHNOTIFICATIONTOKENRESPONSE']._serialized_start=1205
  _globals['_REFRESHNOTIFICATIONTOKENRESPONSE']._serialized_end=1239
  _globals['_SETNICKNAMEREQUEST']._serialized_start=1241
  _globals['_SETNICKNAMEREQUEST']._serialized_end=1261
  _globals['_SETNICKNAMERESPONSE']._serialized_start=1263
  _globals['_SETNICKNAMERESPONSE']._serialized_end=1284
  _globals['_SETSUBSCRIPTIONREQUEST']._serialized_start=1286
  _globals['_SETSUBSCRIPTIONREQUEST']._serialized_end=1310
  _globals['_SETSUBSCRIPTIONRESPONSE']._serialized_start=1312
  _globals['_SETSUBSCRIPTIONRESPONSE']._serialized_end=1337
  _globals['_LOGINSESSION']._serialized_start=1803
  _globals['_LOGINSESSION']._serialized_end=2799
# @@protoc_insertion_point(module_scope)
