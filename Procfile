web: gunicorn informatik22.wsgi --bind 0.0.0.0:$PORT --workers 2 --log-file -
release: python manage.py migrate --noinput && python create_admin.py && python seed_quizzes.py && python manage.py collectstatic --noinput

