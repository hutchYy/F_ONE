import socket,os, platform, time, encrypted_connection
HOST = '0.0.0.0' #Set as every ip address can connect to the server.
PORT = 6969

#Calling the function to set the secret key
encrypter = encrypted_connection.encrypter(b"d41d8cd98f00b205")
#Calling the function to create the TCP server with specified PORT & HOST.
client_ip = encrypter.initialize_tcp_connexion_server(HOST,PORT)

while True:
        command = input(client_ip+ " > ")
        if(command == "quit"):
            break
        else :
            try:
                if(len(command.split()) != 0):
                    encrypter.send_message_server(command)
                    #client_socket.send(command.encode("utf-8"))
                    print(encrypter.receive_message_server())
                    #print(client_socket.recv(2048).decode("utf-8")+"\n")
                else:
                    print("continue")
                    continue
            except(EOFError):
                    print("Invalid input, type 'help' to get a list of implemented commands.\n")
                    continue
encrypter.close_tcp_connexion_server()