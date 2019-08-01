import re

''' Este objeto, segun el apache core, es el que 
despacha los modulos. En mi caso, los recursos
registrados de la aplicacion que va a ir a buscar
para generar el "body" del Response viste... 
A su vez, valida si el recurso existe o no,
valida si es un recurso valido, valida si esta todo bien
 si es forbidden 300, not found resource 404,
 200 OK, 500 internal error '''

class Request:
    ''' Create HTTP Request object from the socket ''' 
    def __init__(self, client_sock):
        self.raw_http_request = False
        self.headers      = {}
        self.metadata     = None
        self.method       = None
        self.uri          = None
        self.http_version = None
        self.resource     = None
        self.content      = None
        self.allowed_methods = ['GET']
        self._get_buffer( client_sock )

    def is_ws_valid(self):
        return self.raw_http_request and self.raw_http_request.find('Upgrade: websocket') >= 0

    def is_method_allowed(self):
        return self.method in self.allowed_methods

    def _get_buffer(self, client_sock):
        ''' get data from socket buffer '''
        data = client_sock.recv(2048).decode()
        if data:
            self.raw_http_request = data
            self._parse()

    def _parse(self):
        self.metadata, self.content = self.raw_http_request.split("\r\n\r\n")
        self.metadata = self.metadata.split("\r\n")
        
        verb = self.metadata[:1]
        self.method, self.uri, self.http_version = re.search(
            '(.*) (/.*) (HTTP/[0-1]{1}\.[0-1]{1})',
            self.metadata[0]
        ).groups()

        # Decompose headers
        header_rows = self.metadata[1:]
        for header_row in header_rows:
            f = header_row.split(":")
            self.headers[f[0]] = f[1].strip()
        