# Import Framework
from src import frontController, Command

# Create My Own Commands
class WhosOnlineCommand(Command):
    def execute(self):
        ''' Lua content '''
        print('ee puto')

class ExitCommand(Command):
    def execute(self):
        print('me fui!!!! jojoiiss')

# Application Setup
if __name__ == "__main__":
    frontController.register_command( 'who', WhosOnlineCommand() )
    frontController.register_command( 'exit', ExitCommand() )
    frontController.run()