import logging

from gateway import settings
from gateway.datapoint import DatapointList


class Message:
    _message_body = list()

    def __init__(self, arbitration_id, message_len, operation_id):
        self._arbitration_id = arbitration_id
        self._message_id = arbitration_id >> 24
        self._device_type = (arbitration_id >> 8) & 0xff
        self._device_id = arbitration_id & 0xff
        self._message_len = message_len >> 3
        self._operation_id = operation_id

    def message_id(self):
        return self._message_id

    def message_len(self):
        return self._message_len

    def operation_id(self):
        return self._operation_id

    def put(self, body):
        if self._operation_id in settings.OPERATIONS:
            self._message_body.append(body)

    def parse_data(self):
        if not self._message_body:
            return None

        data = list()
        point = None
        for body in self._message_body:
            point = body.datapoint
            data.append(body.data)

        if data and point:
            return point.function_name, point.datapoint.datatype.convert(data)
        else:
            logging.debug("No know point found for (%d, %d, %d), len %d", point.function_group,
                          point.function_number, point.function_name, len(data))

        return None


class Response:
    def __init__(self, data):
        datapoint_list = DatapointList()
        function_group = data[2]
        function_number = data[3]
        function_datapoint = int.from_bytes(data[4:6], byteorder='big', signed=False)
        self._datapoint = datapoint_list.get_datapoint(function_group, function_number, function_datapoint)
        self._data = data

    def data(self):
        return self._data

    def datapoint(self):
        return self._datapoint


class Request:
    def __init__(self, operation_id, function_name, data):
        pass