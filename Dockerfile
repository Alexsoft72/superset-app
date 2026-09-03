FROM apache/superset:latest

# Устанавливаем зависимости, если требуется
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Копируем конфигурацию
COPY superset_config.py /app/superset_config.py

# Меняем пользователя на superset
USER superset
