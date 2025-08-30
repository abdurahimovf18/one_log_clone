# Exit immediately if any command returns a non-zero status
set -e

# Run the application using this command
exec uv run python -m src.bot.main
