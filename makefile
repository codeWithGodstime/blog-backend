
makemigrations:
	docker-compose exec backend python manage.py makemigrations

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

shell:
	docker-compose exec backend sh

# Start the Django development server
startserver:
	docker-compose -f local.yml up

# Apply migrations in the backend container
migrate:
	docker-compose exec backend python manage.py migrate