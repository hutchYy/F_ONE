
import socket, encrypted_connection
 
HOST = '0.0.0.0'  # server will bind to any IP
PORT = 12345
encrypter = encrypted_connection.encrypter(b"d41d8cd98f00b204")
encrypter.initialize_tcp_connexion_server(HOST,PORT)
 
 
while True:
    rep = input("Voulez vous envoyer un message ? (y/n/q) : ")
    if rep == "y" :
        message = input("Entrez votre message : ")
        encrypter.send_message_server(message)
        print("Message has been send")

    print("Waiting for message")
    messageRecu = encrypter.receive_message_server()
    print(messageRecu)
 
encrypter.close_tcp_connexion_server