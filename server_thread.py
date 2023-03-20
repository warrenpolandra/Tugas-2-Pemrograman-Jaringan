from socket import *
import socket
import threading
import logging
import time
import sys

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		while True:
			data = self.connection.recv(32)
			if data:
				message = ""
				decoded = data.decode()
				logging.warning(f"Request: {decoded}")
				# Cek apakah request sesuai ketentuan
				if decoded[:4] == "TIME" and decoded[-2:] == '\r\n':
					# Respon TIME dari server
					t = time.localtime()
					currTime = time.strftime("%H:%M:%S", t)
					message = message + "JAM " + currTime + "\r\n"
					logging.warning(f"Sending: {message}")
				else:
					# Respon jika request tidak sesuai ketentuan
					message = message + "Unknown Request\r\n"
					logging.warning(f"Sending: {message}")
				self.connection.sendall(message.encode())
			else:
				# JIka request tidak sesuai ketentuan
				message = "Unknown Request\n"
				self.connection.sendall(message.encode())
				break
		self.connection.close()

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		threading.Thread.__init__(self)

	def run(self):
		# Port 45000
		self.my_socket.bind(('0.0.0.0',45000))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()

