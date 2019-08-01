# deberia definir el syspath... para que server log se guarde en logs...
# ARmar los path relativos obvio.. esto tiene q estar en el bin, algo asi ver bien eso me gusta
config = {
  'host': 'localhost',
  'port': 9991,
  'log': {
    'file': '....//logs/server.log',
    'format': "%(asctime)s - %(levelname)s - %(message)s"
  }
}
