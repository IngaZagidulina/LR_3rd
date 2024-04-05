from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Создание базы данных и таблицы пользователей
conn = sqlite3.connect('users.db')
print("База данных открыта успешно")

conn.execute('''CREATE TABLE IF NOT EXISTS users
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT NOT NULL,
       password TEXT NOT NULL)''')
print("Таблица пользователей создана успешно")
conn.close()


# Регистрация нового пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Пожалуйста, укажите имя пользователя и пароль'}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверка наличия пользователя в базе данных
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'message': 'Пользователь с таким именем уже существует'}), 400

    # Хеширование пароля перед сохранением в базу данных
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Пользователь зарегистрирован успешно'}), 201


# Аутентификация пользователя
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Не удалось верифицировать', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Поиск пользователя в базе данных
    cursor.execute("SELECT * FROM users WHERE username=?", (auth.username,))
    user = cursor.fetchone()

    conn.close()

    if not user:
        return make_response('Не удалось верифицировать', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # Проверка пароля
    if check_password_hash(user[2], auth.password):
        # Генерация токена сессии
        token = str(uuid.uuid4())

        # Сохранение токена в базе данных или кэше

        return jsonify({'token': token}), 200

    return make_response('Не удалось верифицировать', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


if __name__ == '__main__':
    app.run(debug=True)

# Этот код предоставляет простой веб-сервер на Flask
# для регистрации пользователей, проверки их аутентификации
# с использованием базы данных SQLite и безопасным хранением 
# паролей в хэшированном формате. Он также генерирует токен
# сессии при успешной аутентификации пользователя.

