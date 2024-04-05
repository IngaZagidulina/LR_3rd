import socket

def echo_server(host, port):
    # Создание TCP сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Привязываем сокет к указанному хосту и порту
        server_socket.bind((host, port))
        print(f"Сервер запущен на {host}:{port}")
        # Начинаем слушать входящие соединения, с максимальным количеством ожидающих соединений равным 5
        server_socket.listen(5)
        print("Начало прослушивания порта...")

        while True:
            # Принимаем входящее соединение
            client_socket, client_address = server_socket.accept()
            print(f"Подключение клиента {client_address}")

            with client_socket:
                while True:
                    # Получаем данные от клиента порциями по 1 КБ
                    data = client_socket.recv(1024)
                    if not data:
                        print("Отключение клиента.")
                        break  # Если данных нет, прекращаем чтение
                    # Отправляем данные обратно клиенту
                    client_socket.sendall(data)
                    print(f"Прием данных от клиента: {data.decode('utf-8')}")
                    print(f"Отправка данных клиенту: {data.decode('utf-8')}")

if __name__ == "__main__":
    HOST = '127.0.0.1'  # localhost
    PORT = 12345  # Произвольный порт, но должен быть доступен
    print("Запуск сервера...")
    echo_server(HOST, PORT)
