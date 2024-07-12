from datetime import datetime

from aiogram.types import User, Chat, ChatMemberUpdated


# Template func for bot notification messages
def answer_message(event_user: User, event_chat: Chat, event_time: datetime, event: ChatMemberUpdated):
    date_format = "%d-%m-%Y"
    time_format = "%X"

    # Show username with more common '@' at the start if the user has one
    if event_user.username is not None:
        username = f'@{event_user.username}'
    else:
        username = event_user.username

    answer_msg = (
        f'User full name: {event_user.full_name}\n'
        f'Username: {username}\n'
        f'User ID: {event_user.id}\n\n'

        f'{event_chat.type.capitalize()} title: {event_chat.title}\n'
        f'{event_chat.type.capitalize()} ID: {event_chat.id}\n\n'

        f'Date: {event_time.strftime(date_format)}\n'
        f'Time (UTC+3): {event_time.strftime(time_format)}'
    )

    return answer_msg
