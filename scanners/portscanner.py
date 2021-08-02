import socket
from threading import Thread


class PortScanner:
    def __init__(self, address):
        self.handlers = []
        self.address = address
        self.scanned = 0
        self.ports_to_scan = 0

    def reset(self):
        self.scanned = 0
        self.ports_to_scan = 0

    def run_event(self, event_name, arg1, arg2):
        for handle in self.handlers:
            if handle.event_type == event_name:
                handle(arg1, arg2)

    def on(self, event_name, handler):
        handler.event_type = event_name
        self.handlers.append(handler)

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.address, port))
        if result == 0:
            self.run_event("port_open", port, sock)
        else:
            self.run_event("port_closed", port, None)
        sock.close()
        self.scanned = self.scanned + 1
        if self.scanned >= self.ports_to_scan:
            self.run_event("end", self.scanned, port)

    def scan_port_async(self, port):
        thread = Thread(target=self.scan_port, args=(port, ))
        thread.start()

    def scan_ports(self, ports):
        self.reset()
        self.ports_to_scan = len(ports)
        for port in ports:
            self.scan_port(port)

    def scan_ports_async(self, ports):
        self.reset()
        self.ports_to_scan = len(ports)
        for port in ports:
            self.scan_port_async(port)
