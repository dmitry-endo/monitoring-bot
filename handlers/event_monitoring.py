from pytz import timezone

from aiogram import Router, Bot
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION, PROMOTED_TRANSITION, IS_ADMIN, MEMBER, RESTRICTED, IS_MEMBER
from aiogram.types import ChatMemberUpdated

# Load ID with the specified chat for notifications
from config import NOTIF_CHAT_ID
from .answer_template import answer_message

router = Router()

utc_plus3 = timezone("Europe/Moscow")


# Handler for join or promotion as an Admin events
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
                  f'{answer_message(user, chat, local_event_datetime, event)}')
        )
    else:
        await bot.send_message(
            chat_id=NOTIF_CHAT_ID,
            text=(f'Someone joined a {chat.type} as an Admin!\n\n'
                  f'{answer_message(user, chat, local_event_datetime, event)}')
        )


# Handler for join as common member events
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
              f'{answer_message(user, chat, local_event_datetime, event)}')
    )


# Handler for demotion as an Admin events
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
              f'{answer_message(user, chat, local_event_datetime, event)}')
    )


# Handler for leaving members events
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
              f'{answer_message(user, chat, local_event_datetime, event)}')
    )
