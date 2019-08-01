import hashlib
import base64

from .communication import CommunicationHandler

MAGIC_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
available_commands = {} #command supplier..

def create_handshake( key ):
    ''' Create a websocket valid handshake based on rfc6455#section-5.2 '''
    combined = key + MAGIC_GUID
    return base64.b64encode( hashlib.sha1( combined.encode() ).digest() ).decode()


# Cambiar el nombre a esto, es horrible... no va
class WebSocket:
    @staticmethod
    def auth( request, response ):
        ''' Validate if is a WebSocket Request and create a WebSocket Accept Response if is ok '''
        if request.is_ws_valid():
            response.setStatusCode(101)
            response.append_header('Upgrade', 'WebSocket')
            response.append_header('Connection', 'Upgrade')
            response.append_header('Sec-WebSocket-Accept', create_handshake( request.headers['Sec-WebSocket-Key'] ))
            response.append_header('Content-Type', 'application/json')
            
            return response
        else:
            return False
    
    @staticmethod
    def start( client ):
        ''' Start a communication thread with the client that knows how to talk WebSocket Rock..'''
        CommunicationHandler( client, [ WebSocket.execute_command, WebSocket.is_command_available ] )

    @staticmethod
    def add_command( name, command ):
        available_commands[ name ] = command

    @staticmethod
    def is_command_available( name ):
        return name in available_commands

    @staticmethod
    def execute_command( commandName ):
        return available_commands[ commandName ].execute()
        