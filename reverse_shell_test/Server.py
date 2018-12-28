import socket,os, platform, time, encrypted_connection
HOST = '0.0.0.0' #Set as every ip address can connect to the server.
PORT = 6969

def downloadFile(fileName : str):
    encrypter.send_message_server("dl "+ fileName)
    path = "downloaded_files"
    try :
        if encrypter.DownloadFile(path, fileName):
            print("Download sucessful.")
            os.system("qlmanage -p " + path + "/"+ fileName + ">/dev/null 2>&1" )
        else :
            print("The file you want to download doesn't exist !")
    except :
        print("Problem in definition.")

def uploadFile(fileName : str):
    encrypter.UploadFile(fileName)
    
#Calling the function to set the secret key
encrypter = encrypted_connection.server(b"d41d8cd98f00b205")
#Calling the function to create the TCP server with specified PORT & HOST.
client_ip = encrypter.initialize_tcp_connexion_server(HOST,PORT)

while True:
        command = input(client_ip+ " > ")
        if(command == "quit"):
            break
        elif("dl" in command):
            try :
                command_split = command.split()
                downloadFile(command_split[1])
            except :
                print("No file name !")
        elif(command == "upload"):
            if os.path.isfile("up.txt") :
                encrypter.send_message_server("upload")
                uploadFile("up.txt")
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