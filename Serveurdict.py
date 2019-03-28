# _*_ coding: utf-8 _*_
from socket import * # sockets
from threading import Thread # thread
import sys
import os
import random

#stocke les infos sur les clients
clients = {}
#stocke les clients en recherche
research = {}
#stocke les clients qui sont ou ont été dans un chat privé
privateChat = {}
 
def listClients():
	while 1:
		somethin = raw_input('Voulez vous voir la liste des clients connectés (list) ou fermer le serveur (close) ?\n')
		#list all available connections
		if somethin == "list":
			if len(clients) !=0:
				for i in clients.keys():
						print "name: %s ip: %s port: 12000"%(i,clients[i][1])
			else: 
				print "Pas de clients connectés" 	

		elif somethin == "research":
			if len(research) !=0:
				for i in research.keys():
						print "name: %s ip: %s port: 12000"%(i,clients[i][1])
			else: 
				print "Pas de clients en recherche" 	

		elif somethin == "private":
			if len(privateChat) !=0:
				for i in privateChat.keys():
						print "name: %s ip: %s port: 12000"%(i,clients[i][1])
			else: 
				print "Pas de clients en privé" 			
					
		elif somethin == "close":
			for i in clients.keys():
				try:
					clients[i][0].send("close")
				except:
					print "Logged out client"
			break
	serverSocket.close()	
	os._exit(0)
	sys.exit("Finished Execution")

def clientManager(name):
	identification = "Client %s est connecté." % (name)
	print identification
	for i in clients.keys():
			clients[i][0].send(identification)
	while 1:	
		try:
			message = clients[name][0].recv(1024) # 
		except:
			os._exit(0)	
		if not message:
			break
		serv_response = "%s sent: %s" % (name,message)
		#stocke l'id du client qui a envoyé le message
		clientSender = name
		print serv_response

		if name in privateChat.keys() :

			if message == "start":
					clients[name][0].send("Vous êtes déjà en recherche ou en conversation privée.")

			elif message == "next":
				research[name]=clients[name][0]
				research[privateChat[name][1]]=clients[privateChat[name][1]]
				del privateChat[privateChat[name][1]]
				del privateChat[name]
			
			elif message == "lobby":
				research[privateChat[name][1]]=clients[privateChat[name][1]]
				del privateChat[privateChat[name][1]]
				del privateChat[name]

			elif message != "close":
				clients[privateChat[name][1]][0].send(serv_response)
		
		else :		

			if message == "start":
				if name not in research.keys():
					clients[name][0].send("Vous cherchez un ami.")
					research[name]=clients[name][0]
				else :
					clients[name][0].send("Vous êtes déjà en recherche ou en conversation privée.")

			elif message == "next":
				clients[name][0].send("Vous n'êtes pas encore en privé.")
			
			elif message == "lobby":
				if name in research.keys():
					del research[name]
				else :
					clients[name][0].send("Vous êtes déjà dans l'accueil.")

			elif message == "close":
				serv_response = "Client %s left the room."%name
				print "Client %s left the room."%name
				for i in clients.keys():
						clients[i][0].send(serv_response)	
				break

			else :
				for i in clients.keys():
					if i != clientSender and i not in privateChat.keys():
						clients[i][0].send(serv_response)

		if len(research)>=3:
			a = random.randint(0,len(research)-1)
			b = int(a)
			while b==a:
				b = random.randint(0,len(research)-1)
			client1 = research.keys()[a]
			client2 = research.keys()[b]
			privateChat[client1]=[client1,client2]
			privateChat[client2]=[client2,client1]
			clients[client1][0].send("You are in a private chat with %s" %(client2))
			clients[client2][0].send("You are in a private chat with %s" %(client1))
			del research[client1]
			del research[client2]
			
	print(clients[name][0])		
	clients[name][0].close()
	del clients[name]


serverName = '' # server ip
serverPort = 12000 # port
global serverSocket
serverSocket = socket(AF_INET,SOCK_STREAM) # TCP socket
try:
	serverSocket.bind((serverName,serverPort))
except:
	print "Port already in use"
	serverSocket.close()
	os._exit(0)
t = Thread(target=listClients, args=())
t.start()
serverSocket.listen(1) 
print "TCP server waiting connections on port %d ..." % (serverPort)
while 1:
	try:
		connectionSocket, addr = serverSocket.accept()
		connectionSocket.send("Votre pseudo ?")
		nom = True
		while nom == True :
			nom = False
			sentence = connectionSocket.recv(1024) 
			if sentence in clients.keys():
					nom = True
					connectionSocket.send("Nom déjà utilisé, choisissez en un nouveau :")
					break
	except:
		serverSocket.close()
		os._exit(0)
	clients[sentence]=[connectionSocket,addr]
	test = Thread(target=clientManager, args=(sentence,))
	test.start()
serverSocket.close() 


