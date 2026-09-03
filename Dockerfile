# Базовый образ Superset
FROM apache/superset:latest

# Копируем файл с зависимостями
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install -r /app/requirements.txt

# Копируем конфигурационный файл
COPY superset_config.py /app/superset_config.py

# Устанавливаем переменную окружения, чтобы Superset знал, где искать конфиг
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

# Переключаемся на пользователя superset (безопасность)
USER superset
