# Запуск приложения
1. docker-compose up
2. Перейти по сслыке в браузере: http://localhost:8000/login

# Запуск тестов
1. Создать виртуальное окружение: py(python, python3) -m venv vevn
2. Войти в виртуальное окружение
3. Для windows (GIT Bash): source ./venv/Scripts/activate, (posershell): .\venv\Scripts\activate
4. Для linux: source ./venv/bin/activate
5. Создать .env файл с содержимым: 
APP_CONF__DB__URL = postgresql+asyncpg://Arseniy:12345@127.0.0.1:5434/images
APP_CONF__REDIS__URL = redis://localhost:6379/0
APP_CONF__RABBITMQ__URL = amqp://user:password@localhost:5672
APP_CONF__RUN__HOST = localhost
APP_CONF__RUN__PORT = 8000
6. pytest test_image_functions.py - запуск unit-тестов
# Пользователи для логина в системе
Nick: ars, pass: 123
Nick: art, pass: 1234
Nick: tim, pass: 321