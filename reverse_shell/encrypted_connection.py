from Crypto.Cipher import AES
import socket, time
class encrypter:
    nonce = []
    def __init__(self, hash) :
        super().__init__()
        self.hash = hash

    def initialize_tcp_connexion_server(self, HOST, PORT):
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
    def initialize_tcp_connexion_client(self, HOST, PORT):
        global connexion_socket
        connexion_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connexion_socket.connect((HOST, PORT))
        print("\n[*] Connected to " +HOST+ " on port " +str(PORT)+ ".\n")

    def close_tcp_connexion_server(self):
        client_socket.close()
    def close_tcp_connexion_client(self):
        connexion_socket.close()

    def encrypt(self, raw, mode):
        cipher = AES.new(self.hash, AES.MODE_EAX)
        self.nonce = cipher.nonce
        if mode == "picture":
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
            cipher.verify(tag)
            if mode == "picture":
                return decypherText
            else:
                plaintext = decypherText.decode("utf-8")
                return plaintext
        except:
            print("Key incorrect or message corrupted")

    def send_message_server(self, raw) :
        encryptedPack = self.encrypt(raw, "message")
        client_socket.send(encryptedPack)
    def send_message_client(self, raw) :
        encryptedPack = self.encrypt(raw, "message")
        connexion_socket.send(encryptedPack)

    def receive_message_server(self) :
        #print("WAITING FOR TCP PACKET")
        cipherPack = client_socket.recv(1024)
        #print("TCP MESSAGE RECEIVED")
        try :
            stringMessage = self.decrypt(cipherPack,"message")
            return stringMessage
        except :
            print("WRONG PASSPHRASE, EXITING...")
            return "exit"
    def receive_message_client(self) :
        #print("WAITING FOR TCP PACKET")
        cipherPack = connexion_socket.recv(1024)
        #print("TCP MESSAGE RECEIVED")
        try : 
            stringMessage = self.decrypt(cipherPack, "message")
            return stringMessage
        except :
            print("WRONG PASSPHRASE, EXITING...")
            return "exit"

    def send_picture_client(self, raw) :
        encryptedPack = self.encrypt(raw, "picture")
        connexion_socket.send(encryptedPack)
    def receive_picture_server(self) :  
        cipherPack = client_socket.recv(4096)
        #print("TCP MESSAGE RECEIVED")
        bytesMessage = self.decrypt(cipherPack,"picture")
        return bytesMessage