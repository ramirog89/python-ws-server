WS_HTTP_ENOL = '\r\n' #poner esto en constants

''' Armar los setters y getters bien definidos '''
httpCodes = {
    405: 'Method Now Allowed',
    101: 'Web Socket Protocol Handshake'
}

class Response:
    ''' Create a HTTP Response object correspond
      to RFC and allow to modify, and add extra info '''
    def __init__(self, **args):
        for (key, value) in args.items():
            setattr(self, key, value)

        self._handshake = None
        self._headers = {}
        self._set_headers()
        self._http_version = "HTTP/1.1"
        self._statusCode = 200
        self._statusName = "OK"
    
    def append_header( self, header, value ):
        self._headers[header] = value + WS_HTTP_ENOL
    
    def setStatusCode( self, code ):
        self._statusCode = code
        self._statusName = httpCodes[ code ]

    def build_response( self ):
        http_response = "{Version} {statusCode} {statusName}\r\n".format(
            Version=self._http_version,
            statusCode=self._statusCode,
            statusName=self._statusName)
        
        for key, value in self._headers.items():
            http_response += key + ': ' + value
        http_response += WS_HTTP_ENOL
        return http_response

    def get_response( self ):
        return self.build_response()

    def _set_headers( self ):
        self.append_header('Server', 'SomoNosotroViteh')
        self.append_header('Access-Control-Allow-Origin', 'http://localhost')
        self.append_header('Access-Control-Credentials', 'true')
        # Todo el tiempo, la estuve JODIENDO YO!!!
        # self.append_header('Sec-WebSocket-Extensions', 'permessage-deflate; client_no_context_takeover; server_no_context_takeover')