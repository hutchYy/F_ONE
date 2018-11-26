import socket
class TcpInitialization():
    def __init__(self, HOST, PORT):
        super().__init__()
        self.HOST = HOST
        self.PORT = PORT
    def start (self) :
        global server_socket
        global client_socket
        global client_ip
        global client_port
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crée un serveur tcp
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Aide en cas de perte de connexion
        server_socket.bind((self.HOST, self.PORT))
        server_socket.listen(5)  # Nombre de connexions maximum
        print("\n[*] Listening on port " +str(self.PORT)+ ", waiting for connexions.")
        client_socket, (client_ip, client_port) = server_socket.accept()
        print("[*] Client " +client_ip+ " connected.\n")