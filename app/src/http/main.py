import sys
import socket
import threading
import logging

class Main:
    ''' Main Server Class that init port, create threads per request and holds accepted connections and keep alive service '''
    def __init__(self, host, port):
        self.sock = None
        self.host = host
        self.port = port
        self.create()

    def create(self):
        ''' Create socket '''
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.bind()
            logging.info('Socket created successful')
        except socket.error:
            logging.error('Error on create socket')
            sys.exit()

    def bind(self):
        ''' Bind socket '''
        try:
            print('Starting server...')
            logging.info('starting server...')

            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind( (self.host, self.port) )
            self.listen()
        except socket.error:
            logging.error('Error on bind socket...')
            sys.exit()

    def listen(self):
        ''' Start listening connections '''
        self.sock.listen( 5 )
        print('Listening for connections:')
        logging.info('Listening for connections')

    def accept(self, callback_handler):
        ''' Accept a connection and create a thread to resolve it with a callback '''
        conn, addr = self.sock.accept()
        connection_handler = threading.Thread(
            target=callback_handler,
            args=(conn, ),
            daemon=True
        )
        connection_handler.start()
        log_message = 'Connection stablished with ' + addr[0] + ':' + str(addr[1])
        logging.info( log_message )
        print( log_message )
    
    def shutdown( self ):
        self.sock.close()
        sys.exit()
