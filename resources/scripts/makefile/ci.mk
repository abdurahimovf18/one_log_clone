# === Constants ===
CI_COMPOSE = $(COMPOSE) -f ./docker-compose.yaml -f ./resources/docker/compose/ci.yaml
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

ci-migrate:
	$(CI_EXEC) uv run alembic upgrade head
	