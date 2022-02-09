run:
	python3 manage.py runserver

cleandb:
	rm -rf ./apps/companies/migrations/00*
	rm -rf ./apps/main/migrations/00*
	rm -rf ./apps/moderation/migrations/00*
	rm -rf ./apps/news/migrations/00*
	rm -rf ./apps/notify/migrations/00*
	rm -rf ./apps/resume/migrations/00*
	rm -rf ./apps/users/migrations/00*
	rm -rf ./apps/vacancies/migrations/00*
	rm -rf ./apps/answers/migrations/00*

	rm -rf ./db.sqlite3

	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py dbimport

clndb:
	del ./apps/companies/migrations/00*
	del ./apps/main/migrations/00*
	del ./apps/moderation/migrations/00*
	del ./apps/news/migrations/00*
	del ./apps/notify/migrations/00*
	del ./apps/resume/migrations/00*
	del ./apps/users/migrations/00*
	del ./apps/vacancies/migrations/00*
	del ./apps/answers/migrations/00*

	del ./db.sqlite3

	python manage.py makemigrations
	python manage.py migrate
	python manage.py dbimport

refac:
	isort .
	black -l120 .
