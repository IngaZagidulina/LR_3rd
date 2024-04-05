import socket

def handle_client(connection, address, known_clients):
    client_ip = address[0]
    if client_ip in known_clients:
        connection.sendall(f"С возвращением, {known_clients[client_ip]}!\n".encode())
    else:
        connection.sendall("Привет! Как тебя зовут?\n".encode())
        name = connection.recv(1024).decode().strip()
        known_clients[client_ip] = name
        with open("client_names.txt", "a") as file:
            file.write(f"{client_ip},{name}\n")
        connection.sendall(f"Приятно познакомиться, {name}!\n".encode())
    connection.close()

def main():
    known_clients = {}
    
    # Load known clients from file
    try:
        with open("client_names.txt", "r") as file:
            for line in file:
                client_ip, name = line.strip().split(",")
                known_clients[client_ip] = name
    except FileNotFoundError:
        pass

    HOST = '127.0.0.1'  # localhost
    PORT = 12345        # Arbitrary non-privileged port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print("Сервер слушает...")

        while True:
            connection, address = server_socket.accept()
            print(f"Подключение клиента {address}")
            handle_client(connection, address, known_clients)

if __name__ == "__main__":
    main()
