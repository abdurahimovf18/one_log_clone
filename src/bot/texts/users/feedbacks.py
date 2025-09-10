from src.bot.utils.i18n import gettext as _


def start_feedback():
    return _(
        """
✅ Thank you for choosing to leave feedback!
We’d love to hear from you about:
• 💡 Ideas to help us grow
• 🐞 Bug reports or issues you’ve noticed
• ✨ Personal suggestions about the bot

Please send your message as plain text — every detail helps us improve!
"""
    )


def feedback_accepted():
    return _(
        "✨ Thank you for your feedback! "
        "Your thoughts mean a lot to us. We carefully "
        "review every message and will get back to "
        "you as soon as possible."
    )


def cencel_feedback():
    return _(
        "⬅️ Returning to the main menu."
        "You can share your thoughts about "
        "this bot anytime by leaving feedback."
        "Your ideas are always valuable to us! 💡"
    )


def not_authenticated():
    return _(
        "⚠️ Sorry! This bot can only accept " \
        "feedback from authenticated users."
        "👉 Please authenticate first to continue."    
    )
