import os

# Секретный ключ (будет подставлен из Kubernetes Secret через переменную окружения)
SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY')

# Строка подключения к базе данных (используем SQLite для простоты)
SQLALCHEMY_DATABASE_URI = os.environ.get('SUPERSET_DB', 'sqlite:////app/superset_home/superset.db')

# Отключаем проверку CSRF для простоты (в проде лучше включить)
WTF_CSRF_ENABLED = False

# Отключаем Talisman (защитные заголовки) для простоты работы по HTTP
TALISMAN_ENABLED = False

# Включаем панель администратора
FEATURE_FLAGS = {}

# Настройка отображения
ROW_LIMIT = 5000
SUPERSET_WEBSERVER_PORT = 8088
SUPERSET_WEBSERVER_TIMEOUT = 120
