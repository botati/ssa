from typing import Callable

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from MukeshRobot import DEV_USERS, DRAGONS, pbot


def can_change_info(func: Callable) -> Callable:
    async def non_admin(_, message: Message):
        if message.from_user.id in DRAGONS:
            return await func(_, message)

        check = await pbot.get_chat_member(message.chat.id, message.from_user.id)
        if check.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text(
                ">> أنت لست مسؤولاً ، يرجى الالتزام بحدودك. ⁉️"
            )

        admin = (
            await pbot.get_chat_member(message.chat.id, message.from_user.id)
        ).privileges
        if admin.can_change_info:
            return await func(_, message)
        else:
            return await message.reply_text(
                "ليس لديك أذونات لتغيير معلومات المجموعة ❗️"
            )

    return non_admin


def can_restrict(func: Callable) -> Callable:
    async def non_admin(_, message: Message):
        if message.from_user.id in DEV_USERS:
            return await func(_, message)

        check = await pbot.get_chat_member(message.chat.id, message.from_user.id)
        if check.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text(
                ">> أنت لست مسؤولاً ، يرجى الالتزام بحدودك. ⁉️"
            )

        admin = (
            await pbot.get_chat_member(message.chat.id, message.from_user.id)
        ).privileges
        if admin.can_restrict_members:
            return await func(_, message)
        else:
            return await message.reply_text(
                "ليس لديك أذونات لتقييد المستخدمين في هذه الدردشة."
            )

    return non_admin
