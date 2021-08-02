from scanners.services.ssh import SSH
from scanners.services.http import HTTP


class ServiceScanner:
    def __init__(self):
        self.variables = []
        self.services = [
            SSH(),
            HTTP()
        ]

    def get_modules(self):
        return self.services

    def get_ports(self):
        ports = []
        for service in self.services:
            for port in service.ports:
                ports.append(port)

        return ports

    def get_scanner(self, port):
        for service in self.services:
            if port in service.ports:
                return service

    def push_variables(self, list):
        for variable in list:
            self.variables.append(variable)
