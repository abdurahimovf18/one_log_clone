from src.bot.utils.i18n import gettext as _


def message_info() -> str:
    return _(
"""
♻️Automatic Mailing  💬 — a service to automate message sending:

- Behalf of you;
- To selected groups;;
- In custom interval.

You will save the time and answer the requests easily!

Steps to do that:

1️⃣ Add additional accounts.
2️⃣ Add the message content.
3️⃣ Set the groups.
4️⃣ Set the interval.
5️⃣ Start the message.
"""
    )


def accounts_info() -> str:
    return _(
        "Here are the accounts linked to your profile. " 
        "You can send messages on behalf of these Telegram " 
        "accounts by setting their status to active."
    )


def accounts_not_found() -> str:
    return _(
        "You haven’t registered any accounts yet. Please "
        "add an account in the settings. Once added, "
        "you can activate or deactivate it at any time."
    )


def groups_info() -> str:
    return _(
        "Here are the groups linked to your profile. " 
        "You can send messages on behalf of these Telegram " 
        "groups by setting their status to active."
    )


def groups_not_found() -> str:
    return _(
        "You haven’t added any groups yet. Please "
        "add a group in the settings. Once added, "
        "you can activate or deactivate it at any time."
    )


def message_content_request(current_text: str | None = None) -> str:
    action_info = _("Please enter the message you want to send on behalf of your account.")
    old_text_info = _("The current message is:\n{current_text}")

    current_text = current_text or "-"
    if len(current_text) > 255:
        current_text = f"{current_text[:253]}..."

    return f"{action_info}\n\n{old_text_info.format(current_text=current_text)}"


def message_updated() -> str:
    return _("✅ Your message has been updated successfully.")