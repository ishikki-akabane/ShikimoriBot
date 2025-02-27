

import os
import logging
import asyncio

from telethon import Button
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins

from Shikimori import telethn


@telethn.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
    if event.is_private:
        return await event.respond(
            "__This command can be use in groups and channels!__"
        )

    admins = []
    async for admin in telethn.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        admins.append(admin.id)
    if not event.sender_id in admins:
        return await event.respond("Only admins can mention all!")

    if event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.reply_to_msg_id:
        mode = "text_on_reply"
        msg = event.reply_to_msg_id
        if msg is None:
            return await event.respond(
                "__I can't mention members for older messages! (messages which sended before i added to group)__"
            )
    elif event.pattern_match.group(1) and event.reply_to_msg_id:
        return await event.respond("__Give me one argument!__")
    else:
        return await event.respond(
            "__Reply to a message or give me some text to mention others!__"
        )

    if mode == "text_on_cmd":
        usrnum = 0
        usrtxt = ""
        async for usr in telethn.iter_participants(event.chat_id):
            usrnum += 1
            usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
            if usrnum == 5:
                await telethn.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
                await asyncio.sleep(2)
                usrnum = 0
                usrtxt = ""

    if mode == "text_on_reply":
        usrnum = 0
        usrtxt = ""
        async for usr in telethn.iter_participants(event.chat_id):
            usrnum += 1
            usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
            if usrnum == 5:
                await telethn.send_message(event.chat_id, usrtxt, reply_to=msg)
                await asyncio.sleep(2)
                usrnum = 0
                usrtxt = ""


__mod_name__ = "Tᴀɢɢᴇʀ"

__help__ = """
This Feature helps you to tag every member of your group
  ❍ /mentionall :- Tag every single member of your group. Use it while giving a message or replying to a message

Note :- This Command can mention members upto 10,000 in groups and can mention members upto 200 in channels !
"""
