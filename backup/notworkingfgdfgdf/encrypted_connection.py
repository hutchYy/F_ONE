from Cryptodome.Cipher import AES
import socket, time, os
class encrypter:
    nonce = []
    def __init__(self, hash : bytes) :
        super().__init__()
        self.hash = hash

    def encrypt(self, raw, mode):
        cipher = AES.new(self.hash, AES.MODE_EAX)
        self.nonce = cipher.nonce
        if mode == "raw_data":
            ciphertext, tag = cipher.encrypt_and_digest(raw)
        else:
            ciphertext, tag = cipher.encrypt_and_digest(raw.encode("utf-8"))
        cipherPack = self.nonce + tag + ciphertext
        return cipherPack
    def decrypt(self, cipherPack, mode):
        cipherPackArray = bytearray(cipherPack)
        nonceArray = cipherPackArray[0:16]
        tagArray = cipherPackArray[16:32]
        cipherTextArray = cipherPackArray[32::]
        nonce = bytes(nonceArray)
        tag =  bytes (tagArray)
        cipherText = bytes(cipherTextArray)
        cipher = AES.new(self.hash, AES.MODE_EAX, nonce = nonce)
        decypherText = cipher.decrypt(cipherText)
        try:
            if mode == "raw_data":
                return decypherText
            else:
                cipher.verify(tag)
                plaintext = decypherText.decode("utf-8")
                return plaintext
        except:
            return("Key incorrect, message corrupted or bufferoverflow")
class server:
    keyEncryption = []
    def __init__(self, key : bytes) :
        super().__init__()
        self.keyEncryption = key
        global hideComunnications
        hideComunnications = encrypter(self.keyEncryption)

    def initialize_tcp_connexion_server(self, HOST : int, PORT : int):
        global server_socket
        global client_socket
        global client_ip
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creates server TCP socket
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents from getting timeout issues
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # 5 connections max in queue
        print("\n[*] Listening on port " +str(PORT)+ ", waiting for connexions.")
        # see socket documentation to understand how socket.accept works
        client_socket, (client_ip, client_port) = server_socket.accept()
        print("[*] Client " +client_ip+ " connected.\n")
        return client_ip
    def close_tcp_connexion_server(self):
        client_socket.close()
    
    def send_message_server(self, raw) :
        encryptedPack = hideComunnications.encrypt(raw, "message")
        client_socket.send(encryptedPack)
    def send_raw_data_server(self, raw):
        encryptedPack = hideComunnications.encrypt(raw, "raw_data")
        client_socket.send(encryptedPack)

    def receive_message_server(self) :
        #print("WAITING FOR TCP PACKET")
        cipherPack = client_socket.recv(2048)
        #print("TCP MESSAGE RECEIVED")
        try :
            stringMessage = hideComunnications.decrypt(cipherPack,"message")
            return stringMessage
        except :
            print("WRONG PASSPHRASE, EXITING...")
            return "exit"
    def receive_raw_data_server(self) :  
        cipherPack = client_socket.recv(2048)
        bytesMessage = hideComunnications.decrypt(cipherPack,"raw_data")
        return bytesMessage

    def DownloadFile(self, path, fileName):
        data = b""
        data = self.receive_message_server()
        if str(data) == "downloading" :
            print("Downloading "+fileName+" ...")
            if not os.path.exists(path):
                os.makedirs(path)
            fileToDownload = open(path+"/"+fileName, "wb")
            fileData = bytes(self.receive_raw_data_server())
            fileToDownload.write(fileData)
            while not ("completed" in str(fileData)):
                fileData = self.receive_raw_data_server()
                print(type(fileData), str(fileData))
                fileDataArray = bytearray(fileData)
                if fileDataArray  == b"permissionsfailed" :
                    return False
                if "completed" in str(fileDataArray):
                    fileDataArray  = fileDataArray [:-len("completed")]
                    fileToDownload.write(bytes(fileDataArray ))
                    fileDataArray  = b"completed"
                else :
                    fileToDownload.write(bytes(fileDataArray ))
            fileToDownload.close()
            return True
        else:
            return False
    def UploadFile(self, fileName):
        try:
            fileRead = b""
            if os.path.isfile(fileName) :
                self.send_message_server(("downloading"))
                fileToOpen = open(fileName, "rb")
                fileRead = fileToOpen.read(1024-32)
                while fileRead != b'':
                    self.send_raw_data_server(fileRead)
                    fileRead = fileToOpen.read(1024-32)
                time.sleep(0.5)
                fileToOpen.close()
                self.send_raw_data_server(b"completed")
            else :
                self.send_message_server(b"fileDoesntExist")
        except:
            self.send_message_server(("permissionsfailed"))
class client:
    keyEncryption = []
    def __init__(self, key : bytes) :
        super().__init__()
        self.keyEncryption = key
        global hideComunnications
        hideComunnications = encrypter(self.keyEncryption)

    def initialize_tcp_connexion_client(self, HOST : int, PORT : int):
        global connexion_socket
        connexion_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connexion_socket.connect((HOST, PORT))
        print("\n[*] Connected to " +HOST+ " on port " +str(PORT)+ ".\n")
    def close_tcp_connexion_client(self):
        connexion_socket.close()
    
    def send_message_client(self, raw) :
        encryptedPack = hideComunnications.encrypt(raw, "message")
        connexion_socket.send(encryptedPack)
    def send_raw_data_client(self, raw : bytes) :
        encryptedPack = hideComunnications.encrypt(raw, "raw_data")
        connexion_socket.send(encryptedPack)

    def receive_message_client(self) :
        #print("WAITING FOR TCP PACKET")
        cipherPack = connexion_socket.recv(2048)
        #print("TCP MESSAGE RECEIVED")
        try : 
            stringMessage = hideComunnications.decrypt(cipherPack, "message")
            return stringMessage
        except :
            print("WRONG PASSPHRASE, EXITING...")
            return "exit"
    def receive_raw_data_client(self):
        cipherPack = connexion_socket.recv(1024)
        bytesMessage = hideComunnications.decrypt(cipherPack,"raw_data")
        return bytesMessage
    
    
    def DownloadFile(self, path, fileName):
        data = b""
        data = self.receive_message_client()
        if str(data) == "downloading" :
            print("Downloading "+fileName+" ...")
            if not os.path.exists(path):
                os.makedirs(path)
            fileToDownload = open(path+"/"+fileName, "wb")
            fileData = bytes(self.receive_raw_data_client())
            fileToDownload.write(fileData)
            while not ("completed" in str(fileData)):
                fileData = bytearray(self.receive_raw_data_client())
                if fileData == b'permissionsfailed' :
                    break
                if "completed" in str(fileData):
                    fileData = fileData[:-len("completed")]
                    fileToDownload.write(bytes(fileData))
                    fileData = b"completed"
                else :
                    fileToDownload.write(bytes(fileData))
            fileToDownload.close()
            return True
        else:
            return False
    def UploadFile(self, fileName):
        try:
            fileRead = b""
            if os.path.isfile(fileName) :
                self.send_message_client("downloading")
                fileToOpen = open(fileName, "rb")
                fileRead = fileToOpen.read(2048-32)
                while fileRead != b"":
                    self.send_raw_data_client(fileRead)
                    fileRead = fileToOpen.read(2048-32)
                    if fileRead == b"" :
                        fileRead = b"completed"
                    print(fileRead)
                time.sleep(1)
                fileToOpen.close()
            else :
                self.send_raw_data_client(b"fileDoesntExist")
        except:
            self.send_message_client("permissionsfailed")
    