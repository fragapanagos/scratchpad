import sys
import time
import socket
import errno

HOST = ''
PORT = 12346

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'client: connecting...'
while 1:
	try:
		s.connect((HOST,PORT))
		break
	except socket.error as msg:
		if msg.errno == errno.ECONNREFUSED:
			print 'client: waiting for server...'
			time.sleep(1)
		else:
			raise msg


s.setblocking(0)
data = 'Hello, world'
try:
	while 1:
		print 'client: sending "' + data + '"'
		try:
			s.sendall(data)
		except socket.error as msg:
			if msg.errno == errno.EPIPE:
				print 'client: connection broken. shutting down...'
				s.close()
				sys.exit(0)
			else:
				raise msg
		print 'client: data sent...'
		print 'client: waiting for data...'
		try:
			data = s.recv(1024)
			print 'client: received "' + data + '"'
		except socket.error as msg:
			if msg.errno == errno.EAGAIN:
				print 'client: no data to receive...'
			elif msg.errno == errno.ECONNRESET:
				print 'client: connection reset by peer. shutting down...'
				s.close()
				sys.exit(0)
			else:
				raise msg
		time.sleep(1)
except KeyboardInterrupt:
	print '\nclient: shutting down...'
	s.shutdown(socket.SHUT_RDWR)
	s.close()
