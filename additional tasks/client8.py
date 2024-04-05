import requests

def register(username, password):
    url = 'http://127.0.0.1:5000/register'
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print('Регистрация прошла успешно!')
    else:
        print('Не удалось зарегистрироваться. Пожалуйста, проверьте ваш запрос.')

def login(username, password):
    url = 'http://127.0.0.1:5000/login'
    response = requests.post(url, auth=(username, password))
    if response.status_code == 200:
        token = response.json().get('token')
        print(f'Успешный вход! Ваш токен сессии: {token}')
    else:
        print('Не удалось войти. Пожалуйста, проверьте ваше имя пользователя и пароль.')

if __name__ == '__main__':
    register('user1', 'password1')
    login('user1', 'password1')


# В этом коде метод запроса в функции requests.post, 
# чтобы соответствовать методу POST, 
# который используется на сервере для аутентификации.
# обработаны различные HTTP-статусы ответа для более 
# информативного вывода сообщений о регистрации и входе.