class HTTP:
    def __init__(self) -> None:
        self.service = "HTTP"
        self.variables = []
        self.ports = [80]

    def recognition(self, target, socket):
        socket.send(bytes("GET / HTTP/1.1\nHost: " + target +
                    "\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0\nAccept: text/html, application/xhtml, */*; q=0.01\nAccept-Language: en-US,en;q=0.5\nConnection: keep-alive\n\n", "ascii"))

        data_raw = socket.recv(2048)
        data = repr(data_raw).split('b\'')[1].split('\\r\\n\\r\\n')[0]
        headers = data.split("\\r\\n")

        for header in headers:
            if header != headers[0]:
                key = header.split(":")[0].lower()
                value = header.split(": ")[1]

                if key == "server":
                    return value

        return "unknown"
