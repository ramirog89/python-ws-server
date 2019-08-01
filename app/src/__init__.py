#app es un paquete porque tiene un __init__.py

# Export frontController and Command to the Application Interface in order to setup his Commands
__all__ = ['FrontController', 'Command']

import logging

from .config import config
from .http.server import Server
from .front.controller import FrontController
from .commands.command import Command

#logging.basicConfig(filename=config['log']['file'],
#                    level=logging.DEBUG,
#                    format=config['log']['format'])

httpServer = Server( config['host'], config['port'] )

frontController = FrontController( httpServer )
