import socket

def tcp_client():
    # Запрос имени хоста у пользователя с возможностью установки значения по умолчанию
    while True:
        host_input = input("Введите имя хоста (по умолчанию '127.0.0.1'): ")
        if not host_input:
            HOST = '127.0.0.1'  # Значение по умолчанию
            break
        else:
            HOST = host_input
            break

    # Запрос номера порта у пользователя с возможностью установки значения по умолчанию
    while True:
        port_input = input("Введите номер порта (по умолчанию 12345): ")
        if not port_input:
            PORT = 12345  # Значение по умолчанию
            break
        try:
            PORT = int(port_input)
            if 0 < PORT < 65535:
                break
            else:
                print("Номер порта должен быть в диапазоне от 1 до 65535.")
        except ValueError:
            print("Введите целое число для номера порта.")

    # Создаем TCP сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Подключаемся к серверу
            client_socket.connect((HOST, PORT))
            print(f"Соединение с сервером {HOST}:{PORT} установлено")

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
    tcp_client()
