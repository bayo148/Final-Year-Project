web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn ecommerce_assistant.wsgi:application --bind 0.0.0.0:$PORT
