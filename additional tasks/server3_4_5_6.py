import socket
import logging

def setup_logging():
    logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_available_port(start_port):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp_socket:
                temp_socket.bind(('localhost', start_port))
            return start_port
        except OSError:
            start_port += 1

def echo_server(host, port):
    # Создание TCP сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Привязываем сокет к указанному хосту и порту
        server_socket.bind((host, port))
        logging.info(f"Сервер запущен на {host}:{port}")
        print(f"Сервер запущен на {host}:{port}")
        # Начинаем слушать входящие соединения, с максимальным количеством ожидающих соединений равным 5
        server_socket.listen(5)
        logging.info("Начало прослушивания порта...")
        print("Начало прослушивания порта...")

        while True:
            # Принимаем входящее соединение
            client_socket, client_address = server_socket.accept()
            logging.info(f"Подключение клиента {client_address}")
            print(f"Подключение клиента {client_address}")

            with client_socket:
                while True:
                    try:
                        # Получаем данные от клиента порциями по 1 КБ
                        data = client_socket.recv(1024)
                        if not data:
                            logging.info("Отключение клиента.")
                            print("Отключение клиента.")
                            break  # Если данных нет, прекращаем чтение
                        # Отправляем данные обратно клиенту
                        client_socket.sendall(data)
                        logging.info(f"Прием данных от клиента: {data.decode('utf-8')}")
                        logging.info(f"Отправка данных клиенту: {data.decode('utf-8')}")
                    except ConnectionResetError:
                        logging.info("Соединение с клиентом было разорвано.")
                        print("Соединение с клиентом было разорвано.")
                        break

if __name__ == "__main__":
    HOST = '127.0.0.1'  # localhost

    # Запрос номера порта у пользователя с возможностью установки значения по умолчанию
    while True:
        port_input = input("Введите начальный номер порта (по умолчанию 12345): ")
        if not port_input:
            START_PORT = 12345  # Значение по умолчанию
            break
        try:
            START_PORT = int(port_input)
            if 0 < START_PORT < 65535:
                break
            else:
                print("Номер порта должен быть в диапазоне от 1 до 65535.")
        except ValueError:
            print("Введите целое число для номера порта.")

    AVAILABLE_PORT = find_available_port(START_PORT)
    setup_logging()  # Инициализация логирования
    logging.info(f"Запуск сервера на порту {AVAILABLE_PORT}...")
    echo_server(HOST, AVAILABLE_PORT)
