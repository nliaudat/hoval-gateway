import logging

logging.basicConfig(level=logging.DEBUG)

OPERATIONS = {
    "RESPONSE": 0x42,
    "GET_REQUEST": 0x40,
    "SET_REQUEST": 0x46
}
