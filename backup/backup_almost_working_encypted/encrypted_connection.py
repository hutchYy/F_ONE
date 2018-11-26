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
        if mode == "message" :
            ciphertext, tag = cipher.encrypt_and_digest(raw.encode())
        else :
            ciphertext, tag = cipher.encrypt_and_digest(raw)
        return ciphertext, self.nonce
    def decrypt(self, encrypted, nonce, mode):
        #print("Decyphering the message...")
        try : 
            cipher = AES.new(self.hash, AES.MODE_EAX, nonce = nonce)
            plaintext = cipher.decrypt(encrypted)
            if mode == "message":
                plaintext.decode("utf-8")
            else:
                pass
            #print(encrypted)
            #print(nonce)
            return plaintext
        except:
            print("Can't decypher the message !")

    def send_message_server(self, raw) :
        encryptedPack = self.encrypt(raw, "message")
        client_socket.send(encryptedPack[0])
        time.sleep(0.05)
        #print("TCP MESSAGE")
        client_socket.send(encryptedPack[1])
        #print("TCP NONCE")
    def send_message_client(self, raw) :
        encryptedPack = self.encrypt(raw, "message")
        connexion_socket.send(encryptedPack[0])
        time.sleep(0.05)
        #print("TCP MESSAGE")
        connexion_socket.send(encryptedPack[1])
        #print("TCP NONCE")

    def receive_message_server(self) :
        #print("WAITING FOR TCP PACKET")
        messageRecu = client_socket.recv(2048)
        nonceRecu = client_socket.recv(2048)
        #print("TCP MESSAGE RECEIVED")
        bytesMessage = self.decrypt(messageRecu, nonceRecu, "message")
        try :
            stringMessage = bytesMessage.decode("utf-8")
            return stringMessage
        except :
            print("WRONG PASSPHRASE, EXITING...")
            return "exit"
    def receive_message_client(self) :
        #print("WAITING FOR TCP PACKET")
        messageRecu = connexion_socket.recv(2048)
        nonceRecu = connexion_socket.recv(2048)
        #print("TCP MESSAGE RECEIVED")
        bytesMessage = self.decrypt(messageRecu, nonceRecu, "message")
        try : 
            stringMessage = bytesMessage.decode("utf-8")
            return stringMessage
        except :
            print("WRONG PASSPHRASE, EXITING...")
            return "exit"

    def send_picture_client(self, raw) :
        encryptedPack = self.encrypt(raw, "picture")
        connexion_socket.send(encryptedPack[0])
        #print("TCP MESSAGE")
        connexion_socket.send(encryptedPack[1])
        #print("TCP NONCE")
    def receive_picture_server(self) :  
        messageRecu = client_socket.recv(2048)
        nonceRecu = client_socket.recv(2048)
        #print("TCP MESSAGE RECEIVED")
        bytesMessage = self.decrypt(messageRecu, nonceRecu, "picture")
        stringMessage = bytesMessage
        return stringMessage
