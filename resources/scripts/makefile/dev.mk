# === Constants ===
DEV_COMPOSE = $(COMPOSE) -f ./docker-compose.yaml -f ./resources/docker/compose/dev.yaml
DEV_EXEC = $(DEV_COMPOSE) exec $(EXEC_SERVICE)

# === Docker Compose === 
dev-up: 
	$(DEV_COMPOSE) up -d

dev-down: 
	$(DEV_COMPOSE) down

dev-restart: 
	$(MAKE) dev-down 
	$(MAKE) dev-up

dev-restart-service:
	read -p "<[dev] bash> Enter name of the service (If empty string is entered every service will be restarted): " service; \
	$(DEV_COMPOSE) restart $$service

dev-build: 
	$(DEV_COMPOSE) build

dev-rebuild: 
	$(MAKE) dev-down 
	$(MAKE) dev-build 
	$(MAKE) dev-up

# === Shells ===
dev-service-shell:
	read -p "<[dev] Bash> Enter the service to open the bash: " service;\
	$(DEV_COMPOSE) exec $$service bash

dev-c:
	read -p "<[dev] $(EXEC_SERVICE) /> " command; \
	$(DEV_EXEC) $$command

dev-shell:
	$(DEV_EXEC) bash

dev-database-shell:
	-bash -c 'trap "echo; echo <[dev] database /> Shell interrupted; exit 0" INT'; \
	read -p "<[dev] database /> USER: " user; \
	read -p "<[dev] database /> DATABASE: " database; \
	$(DEV_COMPOSE) exec database psql -U $$user -d $$database

# === Logs ===
dev-show-logs:
	$(DEV_COMPOSE) logs -f

# === Localization/I18n ===
dev-i18n-extract:
	uv run pybabel extract --input-dirs=src/ -o locales/messages.pot

dev-i18n-extract-ext:
	uv run pybabel extract -k _:1,1t -k _:1,2 -k __ --input-dirs=src/ -o locales/messages.pot

dev-i18n-compile:
	uv run pybabel compile -d locales -D messages

dev-i18n-init-lang:
	read -p "Enter language code (e.g., EN, FR, ES, etc.): " lang; \
	lang_upper=$$(echo $$lang | tr '[:lower:]' '[:upper:]'); \
	uv run pybabel init -i locales/messages.pot -d locales -D messages -l $$lang_upper

dev-i18n-update:                   # Update existing translations from .pot
	uv run pybabel update -d locales -D messages -i locales/messages.pot

# === Tests ===
dev-test:
	$(DEV_EXEC) uv run pytest

dev-test-q:
	$(DEV_EXEC) uv run pytest -q

dev-test-:


# === linters ===
dev-lint:
	$(DEV_EXEC) uv run ruff check .

dev-lint-fix:
	$(DEV_EXEC) uv run ruff check . --fix

# === type checks ===
dev-type-check:
	$(DEV_EXEC) uv run pyright

# === linters/tests combination ===
dev-check-code:
	$(MAKE) dev-lint
	$(MAKE) dev-test
	$(MAKE) dev-type-check

# === migrations ===
dev-migrate-stamp:
	$(DEV_EXEC) uv run alembic stamp head

dev-migrate-new:
	read -p "<[dev] $(EXEC_SERVICE) /> Name the revision: " revision_name; \
	$(DEV_EXEC) uv run alembic revision --autogenerate -m "$$revision_name"

dev-migrate-head:
	$(DEV_EXEC) uv run alembic upgrade head
	
dev-migrate-up:
	$(DEV_EXEC) uv run alembic upgrade +1

dev-migrate-down:
	$(DEV_EXEC) uv run alembic downgrade -1

dev-migrate-base:
	$(DEV_EXEC) uv run alembic downgrade base

dev-migrate-to:
	read -p "<[dev] $(EXEC_SERVICE) /> Enter the <revision_id>: " revision_id; \
	$(DEV_EXEC) uv run alembic upgrade $$revision_id

dev-migrations-history:
	$(DEV_EXEC) uv run alembic history --verbose

dev-migrations-current:
	$(DEV_EXEC) uv run alembic current
