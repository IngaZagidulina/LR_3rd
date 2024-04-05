import socket

def tcp_client(host, port):
    # Создаем TCP сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Подключаемся к серверу
            client_socket.connect((host, port))
            print(f"Соединение с сервером {host}:{port} установлено")

            while True:
                # Читаем строку со стандартного ввода
                message = input("Введите сообщение для отправки серверу (для выхода введите 'exit'): ")
                if message.lower() == "exit":
                    break

                # Отправляем сообщение серверу
                client_socket.sendall(message.encode())
                print("Отправка данных серверу:", message)

                # Получаем ответ от сервера
                response = client_socket.recv(1024)
                if not response:
                    print("Разрыв соединения с сервером")
                    break

                print("Прием данных от сервера:", response.decode())

        except ConnectionRefusedError:
            print("Не удалось установить соединение с сервером")

if __name__ == "__main__":
    HOST = '127.0.0.1'  # Адрес сервера
    PORT = 12345        # Порт сервера, к которому подключаемся
    tcp_client(HOST, PORT)
