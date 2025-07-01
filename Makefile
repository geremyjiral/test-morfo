.PHONY: all format lint test

all: format lint test

format:
	uv run black .

lint:
	uv run flake8 .

test:
	uv run pytest
