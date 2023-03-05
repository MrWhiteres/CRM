front:
	cd frontend ; npm run dev

back:
	cd backend; . venv/Scripts/activate; python manage.py runserver

ma:
	cd backend; . venv/Scripts/activate; python manage.py makemigrations

mi:
	cd backend; . venv/Scripts/activate; python manage.py migrate

fr:
	cd backend; . venv/Scripts/activate; pip freeze > requirements.txt

in:
	cd backend; . venv/Scripts/activate; pip install -r requirements.txt