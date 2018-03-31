from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from threading import Thread, Event

from serial_interface.events import *
from serial_interface import serial_interface


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """

    """
    reply = None
    event = None

    def do_GET(self):
        """

        :return:
        """
        request_path = urlparse(self.path)
        print(request_path.path)
        self.event = Event()

        if 'shutdown' in request_path.path:
            shutdown_thread = Thread(target=shutdown, args=(self,))
            shutdown_thread.daemon = True
            shutdown_thread.start()

        elif 'distance' in request_path.path:
            print("HTTP SERVER: Sending get distance command")
            serial_interface.execute_command(self, GET_DISTANCE)

            self.event.wait()
            print("HTTP SERVER: Reply was: ", self.reply)

    def resolve_wait(self, reply=None):
        self.reply = reply
        self.event.set()


def shutdown(handler):
    """

    :param handler:
    :return:
    """
    serial_interface.execute_command(handler, 'shutdown')
    handler.server.shutdown()


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """

    :param server_class:
    :param handler_class:
    :return:
    """
    server_address = ('', 8080)
    server = server_class(server_address, handler_class)
    server.serve_forever()


if __name__ == '__main__':
    serial_interface.start()
    run(handler_class=HTTPRequestHandler)