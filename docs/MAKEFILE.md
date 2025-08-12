# Makefile Commands

This project uses a `Makefile` to simplify common development and localization tasks.
You can run any command by typing:

```bash
make <target>
```

For example:

```bash
make i18n-extract
```

---

## 📦 Internationalization (I18N) Commands

| Command                 | Description                                                                                                                                                          |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `i18n-extract`          | Extracts translatable strings from the `src/` directory into `locales/messages.pot`. Use this when you’ve added new strings but don’t need special keyword handling. |
| `i18n-extract-extended` | Same as above, but also extracts strings using custom keyword patterns: `_:1,1t`, `_:1,2`, `__`. Use when you’re using custom translation function signatures.       |
| `i18n-compile`          | Compiles `.po` translation files in `locales/` into `.mo` binary files for runtime use. Must be run after updating translations.                                     |
| `i18n-add-language`     | Interactively prompts for a language code (e.g., `EN`, `FR`), converts it to uppercase, and initializes a new `.po` file in `locales/`.                              |
| `i18n-update`           | Updates all existing `.po` files with any new strings found in `messages.pot`. Use after extraction when translations already exist.                                 |

### Example Workflow for Adding a New Language

1. Extract all messages:

   ```bash
   make i18n-extract
   ```
2. Add a new language:

   ```bash
   make i18n-add-language
   ```

   *(You’ll be prompted for the language code — enter something like `en` or `FR`.)*
3. Open the new `.po` file in `locales/<LANG>/LC_MESSAGES/messages.po` and translate.
4. Compile translations:

   ```bash
   make i18n-compile
   ```

---

## 🧪 Testing, Linting, and Type Checking

| Command      | Description                                                    |
| ------------ | -------------------------------------------------------------- |
| `test`       | Runs the full pytest suite.                                    |
| `test-quiet` | Runs pytest in quiet mode (minimal output).                    |
| `type-check` | Runs Pyright static type checker on the codebase.              |
| `lint`       | Runs Ruff linter to check for code style issues.               |
| `lint-fix`   | Runs Ruff in auto-fix mode to fix style issues where possible. |
| `check-all`  | Runs `test` and `lint` in sequence to verify code quality.     |

### Example

```bash
make check-all
```

Runs tests and lint checks together — useful before pushing changes.

---

## 🤖 Bot Commands

| Command     | Description                               |
| ----------- | ----------------------------------------- |
| `bot-start` | Starts the bot by running `src.bot.main`. |

### Example

```bash
make bot-start
```

---

## 💡 Notes

* **`uv`** is used as the Python command runner in this project. Make sure it’s installed in your environment before running commands.
* Always run `i18n-compile` after updating `.po` files to ensure translations are available at runtime.
* For new translation keywords, update `i18n-extract-extended` instead of modifying `i18n-extract`.
