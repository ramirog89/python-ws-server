import unittest
from unittest.mock import patch, MagicMock
from src.front.controller import FrontController

@patch('src.http.server.Server')

class TestFrontController(unittest.TestCase):  
    def test_run_application(self, Server):
        self.server = Server #esto tiene que estar mockeado igual...
        self.frontController = FrontController( self.server ) 
        self.server.listen_for_requests.assert_called()

if __name__ == '__main__':
    unittest.main()
