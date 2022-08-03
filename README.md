Инструкция по первичной настройке:

docker-compose -f docker-compose.yml exec movies_app python manage.py flush --no-input

docker-compose -f docker-compose.yml exec movies_app python manage.py migrate

docker-compose -f docker-compose.yml exec movies_app python manage.py collectstatic --noinput