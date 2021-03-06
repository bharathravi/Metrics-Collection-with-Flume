# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='system_status.proto',
  package='flume_metrics',
  serialized_pb='\n\x13system_status.proto\x12\rflume_metrics\"\x7f\n\x0cSystemStatus\x12\x11\n\ttimestamp\x18\x01 \x02(\t\x12\x0c\n\x04host\x18\x02 \x02(\t\x12\x14\n\x0ctotal_memory\x18\x03 \x02(\x04\x12\x13\n\x0b\x66ree_memory\x18\x04 \x02(\x04\x12\x10\n\x08num_cpus\x18\x05 \x02(\r\x12\x11\n\tcpu_usage\x18\x06 \x02(\x02')




_SYSTEMSTATUS = descriptor.Descriptor(
  name='SystemStatus',
  full_name='flume_metrics.SystemStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='timestamp', full_name='flume_metrics.SystemStatus.timestamp', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='host', full_name='flume_metrics.SystemStatus.host', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='total_memory', full_name='flume_metrics.SystemStatus.total_memory', index=2,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='free_memory', full_name='flume_metrics.SystemStatus.free_memory', index=3,
      number=4, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='num_cpus', full_name='flume_metrics.SystemStatus.num_cpus', index=4,
      number=5, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='cpu_usage', full_name='flume_metrics.SystemStatus.cpu_usage', index=5,
      number=6, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=38,
  serialized_end=165,
)

DESCRIPTOR.message_types_by_name['SystemStatus'] = _SYSTEMSTATUS

class SystemStatus(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SYSTEMSTATUS
  
  # @@protoc_insertion_point(class_scope:flume_metrics.SystemStatus)

# @@protoc_insertion_point(module_scope)
