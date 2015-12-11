import os
try:
  from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import SimpleHTTPRequestHandler as Handler
  from http.server import HTTPServer as Server

# Read port selected by the cloud for our application
PORT = int(os.getenv('PORT', 8000))
# Change current directory to avoid exposure of control files
os.chdir('static')
httpd = Server(("", PORT), Handler)
try:
  print("Start serving at port %i" % PORT)
  newpid = os.fork()
  if newpid==0:	#child process
	httpd.serve_forever()
  else:	#parent process	
	execfile('glitchify.py')
except KeyboardInterrupt:
  pass
httpd.server_close()

