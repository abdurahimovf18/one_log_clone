from src.core.domain_schema.shared_schema import ID, ChatID


class UserAuth:
    type user_id = ID
    type chat_id = ChatID
