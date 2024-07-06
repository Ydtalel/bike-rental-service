build:
	docker-compose up --build -d

migrate:
	docker exec -it bike-rental-service-web python manage.py migrate

stop:
	docker-compose down
