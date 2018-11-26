
import socket, encrypted_connection
 
HOST = "localhost"  # attacker's IP adress (this is a random one, just to show you)
PORT = 12345 # attacker's port on which server is listening

encrypter = encrypted_connection.encrypter(b"d41d8cd98f00b204")
encrypter.initialize_tcp_connexion_client(HOST,PORT)
 
while True:
    print("Waiting for message")
    messageRecu = encrypter.receive_message_client()
    print(messageRecu)
    #messageRecu = messageRecu.decode()
    if messageRecu == "Client disconnected." :
        break
    rep = input("Voulez vous envoyer un message ? (y/n/q)")
    if rep == "y" :
        message = input("Entrez votre message : ")
        encrypter.send_message_client(message)
        print("Message has been send")
    elif rep == "q":
        message = "Client disconnected."
        encrypter.send_message_client(message)
        break
    else :
        message = ""
        encrypter.send_message_client(message)
encrypter.close_tcp_connexion_client