.PHONY: up down restart logs clean install lint format test build-base

# Docker Compose shortcuts
build:
	docker-compose build

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

# Developer Tooling
install:
	uv sync --all-packages
	uv run pre-commit install

lint:
	uv run ruff check .
	uv run mypy .

format:
	uv run ruff format .

test:
	uv run pytest

build-base:
	docker build -t pitwall-base:latest -f Dockerfile.base .
