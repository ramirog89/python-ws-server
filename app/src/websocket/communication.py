# Global modules
import sys
import threading

from .decoder import decode
from .encoder import encode

opCodeList = {
    'CLOSE': 8,
    'PING': 9,
    'PONG': 'A'
}

connected_clients = {}

class CommunicationHandler:
    def __init__( self, client, command_handlers ):
        ''' Create a new thread to hold the communication with this guy '''
        connected_clients[ client ] = {}
        self.execute_command, self.is_command_available = command_handlers
        self.start_communication( client )

    def start_communication( self, client ):
        handle_ws_client_request = threading.Thread(
            target=self.ws_client_request,
            args=( client, ),
            daemon=True
        )
        handle_ws_client_request.start()

    def close_communication( self, client ):
        del connected_clients[ client ]
        client.close()

    ''' This class allows to handle websocket connections '''
    def ws_client_request( self, client ):
        ''' This handle each connection to websocket '''
        while not client._closed:
            payload = client.recv(1024)
            opCode  = payload[0] & 15

            if opCode == opCodeList['CLOSE']:
                self.close_communication( client )
            else:
                frame = decode( payload )

                if self.is_command_available( frame ):
                    response = self.execute_command( frame )
                    '''
                    elegir si se hace un broadcast desde el response u algo.. 
                    onda, hacer una mini interfaz de si el response devuelve "render"
                    o algo.. una tupla, un diccionario y de acuerdo a eso:
                    retorno un diccionario algo asi como:
                        {
                            /// Chain of Responsability Pattern? ... nose
                            /// Creo que esto, es lo que deberia hacer la user interfaz
                            de acuerdo a lo que necesite.. el command solo ejecuta y responde
                            doBroadcast?: true....
                            response: messageResponse?,
                            otrocommand: execute() ? 
                            otracosa: algo.. nose? me sirve?
                        }
                    
                    '''
                else:
                    message = frame
                    self._send_broadcast( encode( message ), client )

    
    # @TODO: Cambiar el nombre del invoker
    def _send_broadcast( self, data, invoker ):
        ''' Send response to each successful connection that has been authenticated '''
        for client in connected_clients:
            ''' Reveer esto, broadcast es A TODOS .. 
                quizas para que no le envie el mensaje al que lo esta enviando...
                una vez conectado.. deberia depender del tipo de broadcast.. ajam.. agregar un flag type? '''
            if client != invoker:
                try:
                    client.send( data )
                except:
                    print('Error on send message to socket: ...')
                    print(sys.exc_info())
                    ''' Tira bad file descriptor, para mi es de esta clase
                        no se en que part pero buen '''
