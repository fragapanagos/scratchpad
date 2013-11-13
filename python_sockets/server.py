import sys
import time
import socket
import errno

HOST = ''
PORT = 12346

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
print 'server: waiting for connection...'
try:
	conn, addr = s.accept()
except KeyboardInterrupt:
	print '\nserver: aborting...'
	sys.exit(0)

print 'Connected to', addr
s.close()

conn.setblocking(0)
try:
	while 1:
		print 'server: waiting for data...'
		try:
			data = conn.recv(1024)
			print 'server: received "' + data + '"'
		except socket.error as msg:
			if msg.errno == errno.EAGAIN:
				print 'server: no data to receive...'
			elif msg.errno == errno.ECONNRESET:
				print 'server: connection reset by peer. shutting down...'
				conn.close()
				sys.exit(0)
			else:
				raise msg

		print 'server: sending "' + data + '"'
		try:
			conn.sendall(data)
		except socket.error as msg:
			if msg.errno == errno.EPIPE:
				print 'server: connection terminated, shutting down...'
				conn.close()
				sys.exit(0)
			else:
				raise msg
		print 'server: data sent...'
		time.sleep(1)
except KeyboardInterrupt:
	print '\nserver: shutting down...'
	conn.shutdown(socket.SHUT_RDWR)
	conn.close()
