dev:
	fastapi dev main.py

format:
	isort .
	ruff format .

lint:
	ruff check .

all: format lint