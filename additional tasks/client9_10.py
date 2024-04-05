import socket
import struct

class ExtendedSocket(socket.socket):
    def send_message(self, message):
        # Преобразование строки в байтовый массив
        message_bytes = message.encode('utf-8')
        # Получаем длину сообщения и преобразуем её в байты
        message_length = len(message_bytes)
        length_bytes = struct.pack('!I', message_length)
        # Отправляем длину сообщения в виде заголовка
        self.sendall(length_bytes)
        # Отправляем само сообщение
        self.sendall(message_bytes)

    def receive_message(self):
        # Получаем длину сообщения из заголовка (4 байта)
        length_bytes = self.recv(4)
        if not length_bytes:
            return None
        # Распаковываем длину сообщения из байтов в число
        message_length = struct.unpack('!I', length_bytes)[0]
        # Читаем сообщение
        message_bytes = b''
        while len(message_bytes) < message_length:
            chunk = self.recv(message_length - len(message_bytes))
            if not chunk:
                return None
            message_bytes += chunk
        # Преобразуем байтовый массив в строку
        message = message_bytes.decode('utf-8')
        return message

def main():
    # Создаем сокет и подключаемся к серверу
    client_socket = ExtendedSocket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    # Создаем экземпляр расширенного сокета на основе соединения
    client_extended = ExtendedSocket(fileno=client_socket.fileno())

    while True:
        # Отправляем сообщение
        message = input("Введите сообщение для сервера: ")
        client_extended.send_message(message)

        # Принимаем ответное сообщение
        received_message = client_extended.receive_message()
        if received_message is None:
            print("Сервер отключился.")
            break
        print("Получено от сервера:", received_message)

    # Закрываем соединение
    client_extended.close()

if __name__ == "__main__":
    main()
