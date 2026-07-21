.PHONY: up down restart logs clean

# Docker Compose shortcuts
up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose down && docker-compose up -d

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
