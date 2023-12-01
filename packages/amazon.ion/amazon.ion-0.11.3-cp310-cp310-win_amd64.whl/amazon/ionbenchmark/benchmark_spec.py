# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import os
from os import path
from pathlib import Path

import amazon.ionbenchmark.ion_load_dump as _ion_load_dump

from amazon.ion.simple_types import IonPySymbol


# Global defaults for CLI test specs
_tool_defaults = {
    'iterations': 100,
    'warmups': 0,
    'io_type': 'buffer',
    'command': 'read',
    'api': 'load_dump',
}


class BenchmarkSpec(dict):
    """
    Describes the configuration for a micro benchmark.

    Contains functions for retrieving values that are common to all, and allows dictionary-like access for additional
    parameters.
    
    Benchmark spec files are a stream of one or more Ion structs that describe a benchmark to be run.
    
    Cross-implementation, cross-format fields include `format`, `input_file`, `command`, `api`, `iterations`, `warmups`,
    `name`, and `io_type`.
    Implementation-specific benchmark fields should include a language prefix. For ion-python, the prefix is 'py'.
    Fields that are cross-format but specific to ion-python include `py_c_extension` and `py_gc_disabled`.
    Some data formats have format-specific fields. For example, protobuf has `protobuf_descriptor_file` and 
    `protobuf_type`.
    Finally, there are some fields that are specific to a particular format and implementation, such as 
    `protobuf_py_file` and `protobuf_py_module`.

    The following is a list of all fields supported by ion-python:
     * `name` - a name to use in the test report
     * `format` - the format to use for the benchmark. Can be `ion_text`, `ion_binary`, or another format that is
       supported by an implementation. ion-python supports `json`, `ujson`, `simplejson`, `rapidjson`, `cbor`, `cbor2`,
       `protobuf`, and `self_describing_protobuf`.
       This should really be named something else, like `encoder` since it's a particular implementation for a data
       format that is being tested rather than the data format itself, but it is called `format` so that it is the same
       as the corresponding CLI option for the `read` and `write` commands.
     * `input_file` – the path for a file containing the input data for this benchmark. Can be an absolute path, or the
       path can be relative to the location of the spec file.
     * `command` – one of `read` or `write`
     * `api` – can be `load_dump` or `streaming`
     * `io_type` – can be `buffer` or `file`
     * `iterations` – the total number of iterations the test should take. This does not necessarily correspond to a
       single invocation of the API being tested—rather it is the number of _samples_ that should be measured for the
       benchmark statistics.
     * `warmups` – the number of times the API should be invoked in order to warm up the runtime environment before
       measuring any sample runs.
     * `py_c_extension` – whether the C-extension should be used. (This may be ignored if C extensions are not supported
       by the currently running Python interpreter.) Default: true.
     * `py_gc_disabled` – whether garbage collection should be disabled (paused) for the duration of each benchmark
       sample. Default: false.
     * `protobuf_type` – the name of the protocol buffer type to use from the provided protocol buffer schema
     * `descriptor_file` – A protocol buffer schema in the form of a `FileDescriptorSet` (generated by `protoc`
       using the `--descriptor_set_out` option) that contains the necessary schema for reading/writing the protobuf
       input file.
     * `py_module` – A Python module path pointing to the module, generated by `protoc`, that contains the type
       required to read/write the given input file.
     * `py_file` – A file path pointing to the Python module, generated by `protoc`, that contains the type
       required to read/write the given input file.

    Note—for the `protobuf` format, the `protobuf_type` field and at least one of `descriptor_file`, `py_module`, or
    `py_file` must be provided.
    """
    _data_object = None
    _loader_dumper = None
    _spec_working_directory = None

    def __init__(self, params: dict, user_overrides: dict = None, user_defaults: dict = None, working_directory=None):
        """
        Construct a new BenchmarkSpec, possibly incorporating user supplied defaults or overrides.

        Between the various dicts of parameters, the fields "format", "input_file", "command", "api", "iterations",
        "warmups", and "io_type" must all have a value.

        :param params: Values for this benchmark spec.
        :param user_overrides: Values that override all other values.
        :param user_defaults: Values that override the tool defaults, but not the `params`.
        :param working_directory: reference point to use if `input_file` is a relative path. Defaults to os.getcwd().
        """
        if user_defaults is None:
            user_defaults = {}
        if user_overrides is None:
            user_overrides = {}

        self._spec_working_directory = working_directory or os.getcwd()

        merged = { **_tool_defaults, **user_defaults, **params, **user_overrides }

        # Convert symbols to strings
        for k in merged.keys():
            if isinstance(merged[k], IonPySymbol):
                merged[k] = merged[k].text

        # If not an absolute path, make relative to the working directory.
        input_file = merged['input_file']
        if not path.isabs(input_file):
            input_file = path.join(self._spec_working_directory, input_file)
            merged['input_file'] = input_file

        super().__init__(merged)

        for k in ["format", "input_file", "command", "api", "iterations", "warmups", "io_type"]:
            if self[k] is None:
                raise ValueError(f"Missing required parameter '{k}'")

        if 'name' not in self:
            self['name'] = f'({self.get_format()},{self.derive_operation_name()},{path.basename(self.get_input_file())})'

    def __missing__(self, key):
        # Instead of raising a KeyError like a usual dict, just return None.
        return None

    def get_attribute_as_path(self, key: str):
        """
        Get value from the backing dict, assuming that it is a file path, and appending it to the spec working directory
        if it is a relative path.
        """
        value = self[key]
        if path.isabs(value):
            return value
        else:
            return path.join(self._spec_working_directory, value)

    def get_name(self):
        """
        Get the name of the BenchmarkSpec. If not provided in __init__, one was generated based on the params provided.
        """
        return self["name"]

    def get_format(self):
        return self["format"]

    def get_input_file(self):
        return self["input_file"]

    def get_command(self):
        return self["command"]

    def get_api(self):
        return self["api"]

    def get_io_type(self):
        return self["io_type"]

    def get_iterations(self):
        return self["iterations"]

    def get_warmups(self):
        return self["warmups"]

    def derive_operation_name(self):
        match_arg = [self.get_io_type(), self.get_command(), self.get_api()]
        if match_arg == ['buffer', 'read', 'load_dump']:
            return 'loads'
        elif match_arg == ['buffer', 'write', 'load_dump']:
            return 'dumps'
        elif match_arg == ['file', 'read', 'load_dump']:
            return 'load'
        elif match_arg == ['file', 'write', 'load_dump']:
            return 'dumps'
        else:
            raise NotImplementedError(f"Argument combination not supported: {match_arg}")

    def get_input_file_size(self):
        return Path(self.get_input_file()).stat().st_size

    def get_data_object(self):
        """
        Get the data object to be used for testing. Used for benchmarks that write data.
        """
        if not self._data_object:
            loader = self.get_loader_dumper()
            with open(self.get_input_file(), "rb") as fp:
                self._data_object = loader.load(fp)
        return self._data_object

    def get_loader_dumper(self):
        """
        :return: an object/class/module that has `dump`, `dumps`, `load`, and `loads` for the given test spec.
        """
        if not self._loader_dumper:
            self._loader_dumper = self._get_loader_dumper()
        return self._loader_dumper

    def _get_loader_dumper(self):
        data_format = self.get_format()
        if data_format == 'ion_binary':
            return _ion_load_dump.IonLoadDump(binary=True, c_ext=self['py_c_extension'])
        elif data_format == 'ion_text':
            return _ion_load_dump.IonLoadDump(binary=False, c_ext=self['py_c_extension'])
        elif data_format == 'json':
            import json
            return json
        elif data_format == 'ujson':
            import ujson
            return ujson
        elif data_format == 'simplejson':
            import simplejson
            return simplejson
        elif data_format == 'rapidjson':
            import rapidjson
            return rapidjson
        elif data_format == 'cbor':
            import cbor
            return cbor
        elif data_format == 'cbor2':
            import cbor2
            return cbor2
        elif data_format == 'self_describing_protobuf':
            from self_describing_proto import SelfDescribingProtoSerde
            # TODO: Consider making the cache option configurable from the spec file
            return SelfDescribingProtoSerde(cache_type_info=True)
        elif data_format == 'protobuf':
            import proto
            type_name = self['protobuf_type']
            if not type_name:
                raise ValueError("protobuf format requires the type to be specified")
            if self['py_module']:
                message_type = proto.get_message_type_from_py(type_name, self['py_module'])
            elif self['py_file']:
                message_type = proto.get_message_type_from_py(type_name, "imported_protobuf_module",
                                                              self.get_attribute_as_path('py_file'))
            elif self['descriptor_file']:
                message_type = proto.get_message_type_from_descriptor_set(type_name, self.get_attribute_as_path('descriptor_file'))
            else:
                raise ValueError("format 'protobuf' spec requires py_module, py_file, or descriptor_file")
            return proto.ProtoSerde(message_type)
        else:
            return None
