
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


# ------------------------------------------------------------------------
# Bot commands
# ------------------------------------------------------------------------
bot-start:
	uv run python -m src.bot.main
