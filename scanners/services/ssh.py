class SSH:
    def __init__(self) -> None:
        self.service = "SSH"
        self.variables = []
        self.ports = [22]

    def recognition(self, socket):
        socket.send(bytes(
            "SSH-2.0-8.48 FlowSsh: Bitvise SSH Client (Tunnelier) 8.48 - BvSsh", "ascii"))

        data_raw = socket.recv(1024)
        data = repr(data_raw).split('b\'')[1].split('\\r\\n\'')[0]

        ssh_version = data.split(" ")[0]
        self.variables.append("OS Version=" + data.split(" ")[1])
        return ssh_version
