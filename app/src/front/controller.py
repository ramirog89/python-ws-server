from ..http.request import Request
from ..http.response import Response
from ..websocket.websocket import WebSocket
from ..commands.command import Command

class FrontController:
    def __init__(self, Server):
        self.server    = Server
        self.request   = None
        self.response  = Response()

    def register_command(self, name, command ):
        if isinstance( command, Command ):
            WebSocket.add_command( name, command )
        else:
            raise ValueError(name + 'callback is not a implementing Command Interface')

    
    def dispatcher(self, client):
        # aca estoy recibiendo el conn del accept del server..
        # faltaria el addr, para saber que Socket se desconecto y pasarselo a communication object  
        self.request = Request( client )

        if not self.request.is_method_allowed():
            self.response.setStatusCode(405) # Method not allowed
            self.server.send( client, self.response.get_response().encode() )
            self.server.close_connection( client )
        else: 
            # Auth through WebSocket
            if WebSocket.auth( self.request, self.response ):
                WebSocket.start( client ) # Start the thread for current connection
                ''' Aca tiene que haber un REsponse HTTP que haga 300, 400, 500 etc.. dependiendo y todos sus cases '''
                self.server.send( client, self.response.get_response().encode() )
            else:
                print('Could not authenticate request')
                self.server.close_connection( client )
  
    def run(self):
        ''' Run the server and listeng for messages '''
        self.server.listen_for_requests( self.dispatcher )
