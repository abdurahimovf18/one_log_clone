# # # Setting up Makefile behavior
.SILENT:

### Constants
### ------------------------------------------------------------------------
EXEC_SERVICE = exec-service


### Development Commands
### ------------------------------------------------------------------------

# docker compose file which will be working with is: 
#
# >>> docker compose -f ./docker-compose.yaml -f ./resources/docker/compose/dev.yaml

# === Constants ===
DEV_COMPOSE = docker compose -f ./docker-compose.yaml -f ./resources/docker/compose/dev.yaml
DEV_EXEC = $(DEV_COMPOSE) exec $(EXEC_SERVICE)

# === Docker Compose === 
dev-up: 
	$(DEV_COMPOSE) up -d

dev-down: 
	$(DEV_COMPOSE) down

dev-restart: dev-down dev-up

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
	$(DEV_EXEC) uv run pybabel extract --input-dirs=src/ -o locales/messages.pot

dev-i18n-extract-ext:
	$(DEV_EXEC) uv run pybabel extract -k _:1,1t -k _:1,2 -k __ --input-dirs=src/ -o locales/messages.pot

dev-i18n-compile:
	$(DEV_EXEC) uv run pybabel compile -d locales -D messages

dev-i18n-init-lang:
	read -p "Enter language code (e.g., EN, FR, ES, etc.): " lang; \
	lang_upper=$$(echo $$lang | tr '[:lower:]' '[:upper:]'); \
	$(DEV_EXEC) uv run pybabel init -i locales/messages.pot -d locales -D messages -l $$lang_upper

dev-i18n-update:                   # Update existing translations from .pot
	$(DEV_EXEC) uv run pybabel update -d locales -D messages -i locales/messages.pot

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



### CI Commands
### ------------------------------------------------------------------------

# docker compose file which will be working with is: 
#
# >>> docker compose -f ./docker-compose.yaml -f ./resources/docker/compose/ci.yaml

# === Constants ===
CI_COMPOSE = docker compose -f ./docker-compose.yaml -f ./resources/docker/compose/ci.yaml
CI_EXEC = $(CI_COMPOSE) exec $(EXEC_SERVICE)

# === Docker Compose === 
ci-up:
	$(CI_COMPOSE) up -d

ci-build:
	$(CI_COMPOSE) build

ci-test:
	$(CI_EXEC) uv run pytest --quiet

ci-type-check:
	$(CI_EXEC) uv run pyright

ci-lint:
	$(CI_EXEC) uv run ruff check .
