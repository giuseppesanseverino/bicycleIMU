"""A mock implementation of the BicycleSensor class for testing purposes."""

from multiprocessing.connection import Connection


class BicycleSensor:
  def __init__(self, bicycleinit: Connection, name: str, args: dict):
    pass

  def ping(self):
    pass

  def send_msg(self, msg):
    if isinstance(msg, dict):
      print("Message:", msg)
    else:
      print("Message:", {'type': 'log', 'level': 'info', 'msg': str(msg)})

  def write_header(self, headers):
    print("Headers:", headers)

  def write_measurement(self, data):
    print("Data:", data)

  def shutdown(self):
    print("Shutting down sensor")
