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
        "Here are your accounts included to your account, " 
        "You can send messages behalf of those telegram accounts by " 
        "setting their status active."
    )


def accounts_not_found() -> str:
    return _(
        "You have not registered any accounts yet. " 
        "Please register and set their status to active, " 
        "before sending your messages."
    )


def message_content_request(current_text: str | None = None) -> str:
    action_info = _("Please enter the message you want to send on behalf of your account.")
    old_text_info = _("The current message is:\n{current_text}")

    current_text = current_text or "-"
    if len(current_text) > 255:
        current_text = f"{current_text[:253]}..."

    return f"{action_info}\n\n{old_text_info.format(current_text=current_text)}"


def new_message_text_set(current_text: str) -> str:
    if len(current_text) > 255:
        current_text = f"{current_text[:253]}..."

    return _(
        "Your message has been updated successfully.\n\nThe new message is:\n{current_text}"
    ).format(
        current_text=current_text
    )