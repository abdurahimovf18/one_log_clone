
# ------------------------------------------------------------------------
# I18N commands
# ------------------------------------------------------------------------
i18n-extract:                  # Extract messages to .pot
	pybabel extract --input-dirs=src/ -o locales/messages.pot

i18n-extract-extended:         # Extract with custom keywords
	pybabel extract -k _:1,1t -k _:1,2 -k __ --input-dirs=src/ -o locales/messages.pot

i18n-compile:                  # Compile .po files to .mo
	pybabel compile -d locales -D messages

i18n-add-language:                 # Add a new language
	@read -p "Enter language code (e.g., EN, FR, ES): " lang; \
	lang_upper=$$(echo $$lang | tr '[:lower:]' '[:upper:]'); \
	pybabel init -i locales/messages.pot -d locales -D messages -l $$lang_upper

i18n-update:                   # Update existing translations from .pot
	pybabel update -d locales -D messages -i locales/messages.pot

# ------------------------------------------------------------------------
# test/lint/type-checker commands
# ------------------------------------------------------------------------
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


## -----------------------------------------------------------------------
## Docker/Docker-Compose executed commands
## -----------------------------------------------------------------------

# Those commands are executed inside a running docker container and
# this affects whole code because of the volumes.

# ------------------------------------------------------------------------
# docker-compose
# ------------------------------------------------------------------------

migrate-stamp:
	docker compose exec bot uv run alembic stamp head

migrate-revision:
	@read -p "Enter migration name: " migration_name; \
	echo "Migration is being sent to alembic as $$migration_name"; \
	docker compose exec bot uv run alembic revision --autogenerate -m "$$migration_name"

database-update:
	docker compose exec bot uv run alembic upgrade head

down:
	docker compose down

build:
	docker compose up -d --build --remove-orphans

up:
	docker compose up -d 

show-logs:
	docker compose logs -f

rebuild: down build

