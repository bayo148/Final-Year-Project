FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && gunicorn ecommerce_assistant.wsgi:application --bind 0.0.0.0:$PORT"]