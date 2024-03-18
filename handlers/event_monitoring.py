from datetime import datetime
from pytz import timezone

from aiogram import Router, Bot
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION, PROMOTED_TRANSITION, IS_ADMIN, MEMBER, RESTRICTED, IS_MEMBER
from aiogram.types import ChatMemberUpdated, User, Chat

### Load ID with specified chat for notifications
from config import NOTIF_CHAT_ID

router = Router()

utc_plus3 = timezone("Europe/Moscow")


# Template func for bot notification messages
def answer_message(event_user: User, event_chat: Chat, event_time: datetime):
    date_format = "%d-%m-%Y"
    time_format = "%X"

    # Show username with more common '@' at the start if user has one
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


### Handler for join as an Admin events
### Or promotion to an Admin events
@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=PROMOTED_TRANSITION
    )
)
async def event_is_admin(event: ChatMemberUpdated, bot: Bot):
    user = event.new_chat_member.user
    chat = event.chat
    # Convert naive time to UTC+3
    local_event_datetime = event.date.astimezone(utc_plus3)

    if event.old_chat_member.status == MEMBER or +RESTRICTED:
        await bot.send_message(
            chat_id=NOTIF_CHAT_ID,
            text=(f"Someone's been promoted to an Admin in a {chat.type}!\n\n"
                  f'{answer_message(user, chat, local_event_datetime)}')
        )
    else:
        await bot.send_message(
            chat_id=NOTIF_CHAT_ID,
            text=(f'Someone joined a {chat.type} as an Admin!\n\n'
                  f'{answer_message(user, chat, local_event_datetime)}')
        )


### Handler for join as common member events
@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=JOIN_TRANSITION
    )
)
async def event_is_member(event: ChatMemberUpdated, bot: Bot):
    user = event.new_chat_member.user
    chat = event.chat
    local_event_datetime = event.date.astimezone(utc_plus3)

    await bot.send_message(
        chat_id=NOTIF_CHAT_ID,
        text=(f'Someone joined a {chat.type}!\n\n'
              f'{answer_message(user, chat, local_event_datetime)}')
    )


### Handler for demotion as an Admin events
@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_ADMIN >> IS_MEMBER
    )
)
async def event_is_not_admin(event: ChatMemberUpdated, bot: Bot):
    user = event.new_chat_member.user
    chat = event.chat
    local_event_datetime = event.date.astimezone(utc_plus3)

    await bot.send_message(
        chat_id=NOTIF_CHAT_ID,
        text=(f"Someone's been demoted as an Admin in a {chat.type}!\n\n"
              f'{answer_message(user, chat, local_event_datetime)}')
    )


### Handler for leaving members events
@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=LEAVE_TRANSITION
    )
)
async def event_is_not_member(event: ChatMemberUpdated, bot: Bot):
    user = event.new_chat_member.user
    chat = event.chat
    local_event_datetime = event.date.astimezone(utc_plus3)

    await bot.send_message(
        chat_id=NOTIF_CHAT_ID,
        text=(f"Someone left from a {chat.type}!\n\n"
              f'{answer_message(user, chat, local_event_datetime)}')
    )
