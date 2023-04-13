front:
	cd frontend ; npm run dev --host

back:
	cd backend; . venv/Scripts/activate; python manage.py runserver

dock:
	docker-compose up --build -d --force-recreate --no-deps

stop:
	docker-compose down ; docker image prune -f

ma:
	docker exec -it Django_API sh -c "python manage.py makemigrations"

mi:
	docker exec -it Django_API sh -c "python manage.py migrate"

su:
	cd backend; . venv/Scripts/activate; python manage.py createsuperuser

fr:
	cd backend; . venv/Scripts/activate; pip freeze > requirements.txt

in:
	cd backend; . venv/Scripts/activate; pip install -r requirements.txt

exec:
	docker exec -it Django_API sh

admin:
	python manage.py createsuperuser
