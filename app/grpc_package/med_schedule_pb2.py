# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: med_schedule.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'med_schedule.proto')
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x12med_schedule.proto\x12\x0cmed_schedule"[\n\x15ScheduleCreateRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfrequency\x18\x03 \x01(\t\x12\x10\n\x08\x64uration\x18\x04 \x01(\t"\'\n\x10ScheduleResponse\x12\x13\n\x0bschedule_id\x18\x01 \x01(\x05"\'\n\x14UserSchedulesRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05"-\n\x15UserSchedulesResponse\x12\x14\n\x0cschedule_ids\x18\x01 \x03(\x05"=\n\x15ScheduleDetailRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x13\n\x0bschedule_id\x18\x02 \x01(\x05"]\n\x16ScheduleDetailResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tfrequency\x18\x02 \x01(\t\x12\x10\n\x08\x64uration\x18\x03 \x01(\t\x12\x10\n\x08schedule\x18\x04 \x03(\t"%\n\x12NextTakingsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05"(\n\nNextTaking\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04time\x18\x02 \x01(\t"@\n\x13NextTakingsResponse\x12)\n\x07takings\x18\x01 \x03(\x0b\x32\x18.med_schedule.NextTaking2\x8e\x03\n\x19MedicationScheduleService\x12W\n\x0e\x43reateSchedule\x12#.med_schedule.ScheduleCreateRequest\x1a\x1e.med_schedule.ScheduleResponse"\x00\x12]\n\x10GetUserSchedules\x12".med_schedule.UserSchedulesRequest\x1a#.med_schedule.UserSchedulesResponse"\x00\x12`\n\x11GetScheduleDetail\x12#.med_schedule.ScheduleDetailRequest\x1a$.med_schedule.ScheduleDetailResponse"\x00\x12W\n\x0eGetNextTakings\x12 .med_schedule.NextTakingsRequest\x1a!.med_schedule.NextTakingsResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'med_schedule_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_SCHEDULECREATEREQUEST']._serialized_start = 36
    _globals['_SCHEDULECREATEREQUEST']._serialized_end = 127
    _globals['_SCHEDULERESPONSE']._serialized_start = 129
    _globals['_SCHEDULERESPONSE']._serialized_end = 168
    _globals['_USERSCHEDULESREQUEST']._serialized_start = 170
    _globals['_USERSCHEDULESREQUEST']._serialized_end = 209
    _globals['_USERSCHEDULESRESPONSE']._serialized_start = 211
    _globals['_USERSCHEDULESRESPONSE']._serialized_end = 256
    _globals['_SCHEDULEDETAILREQUEST']._serialized_start = 258
    _globals['_SCHEDULEDETAILREQUEST']._serialized_end = 319
    _globals['_SCHEDULEDETAILRESPONSE']._serialized_start = 321
    _globals['_SCHEDULEDETAILRESPONSE']._serialized_end = 414
    _globals['_NEXTTAKINGSREQUEST']._serialized_start = 416
    _globals['_NEXTTAKINGSREQUEST']._serialized_end = 453
    _globals['_NEXTTAKING']._serialized_start = 455
    _globals['_NEXTTAKING']._serialized_end = 495
    _globals['_NEXTTAKINGSRESPONSE']._serialized_start = 497
    _globals['_NEXTTAKINGSRESPONSE']._serialized_end = 561
    _globals['_MEDICATIONSCHEDULESERVICE']._serialized_start = 564
    _globals['_MEDICATIONSCHEDULESERVICE']._serialized_end = 962
d=962
