from .main import Main

class Server(Main):
  ''' Server Implementation '''
  def __init__(self, host, port):
    super().__init__(host, port)

  def listen_for_requests(self, dispatch_handler):
    while True:
      self.accept( dispatch_handler )

  def send( self, client_socket, message ):
    ''' Send message to connected client '''
    client_socket.send( message )

  def close_connection( self, client_socket ):
    ''' Close client connection '''
    client_socket.close()
