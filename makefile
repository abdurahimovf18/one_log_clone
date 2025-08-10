.PHONY: test test-q type-check lint lint-fix check-all

test: 
	uv run pytest

test-quiet: 
	uv run pytest -q

type-check: 
	uv run pyright

lint: 
	uv run ruff check .

lint-fix: 
	uv run ruff check . --fix

check-all: test lint
