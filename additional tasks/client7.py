import socket

def main():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 12345        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Подключение к серверу успешно.")

        response = client_socket.recv(1024).decode()
        print(response)

        if "Как тебя зовут?" in response:
            name = input("Введите свое имя: ")
            client_socket.sendall(name.encode())

        response = client_socket.recv(1024).decode()
        print(response)

if __name__ == "__main__":
    main()
