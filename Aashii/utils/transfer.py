"""Functions related to transfering messages and their edits."""

from telegram import Bot, Message as TMessage
from telegram import (
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
)
from telegram.constants import MAX_CAPTION_LENGTH, MAX_MESSAGE_LENGTH
from Aashii.constants import Message
from Aashii.utils.misc import dehtml


def _get_from_tag(message: TMessage, quote: bool):
    from_tag = None

    if quote:
        entity_from = Message.ENTITY_FROM.format(
            USER_ID=message.from_user.id,
            FULL_NAME=message.from_user.full_name,
        )
    else:
        entity_from = "\n"

    if message.forward_sender_name:
        name = message.forward_sender_name
        from_tag = Message.ENTITY_FORWARD_ANONYMOUS.format(
            SENDER_NAME=name, FROM=entity_from
        )
    elif message.forward_from_chat:
        chat_id = message.forward_from_chat.id
        name = message.forward_from_chat.title
        from_tag = Message.ENTITY_FORWARD_CHAT.format(
            FROM_CHAT_ID=chat_id, FROM_CHAT_NAME=name, FROM=entity_from
        )
    elif message.forward_from:
        user_id = message.forward_from.id
        name = message.forward_from.full_name
        from_tag = Message.ENTITY_FORWARD_USER.format(
            FROM_USER_ID=user_id, FROM_FULL_NAME=name, FROM=entity_from
        )
    else:
        from_tag = entity_from

    return from_tag


def _get_media(message: TMessage, caption: str):
    if message.animation:
        return InputMediaAnimation(media=message.animation, caption=caption)
    if message.audio:
        return InputMediaAudio(media=message.audio, caption=caption)
    if message.document:
        return InputMediaDocument(media=message.document, caption=caption)
    if message.photo:
        return InputMediaPhoto(media=message.photo[-1], caption=caption)
    if message.video:
        return InputMediaVideo(media=message.video, caption=caption)


def _get_quotable(message: TMessage, from_tag: str):
    caption, captionable = _validate_caption(message)
    text, send_from = message.text_html_urled, True
    tag_len = len(dehtml(from_tag))

    if not from_tag.strip():
        return text, caption, False

    if message.text and (tag_len + len(message.text) < MAX_MESSAGE_LENGTH):
        text = f"{from_tag}{text}"
        send_from = False
    elif captionable and (tag_len + len(message.caption) < MAX_CAPTION_LENGTH):
        caption = f"{from_tag}{caption}"
        send_from = False

    return text, caption, send_from


def _validate_caption(message: TMessage):
    if (
        message.animation
        or message.audio
        or message.document
        or message.photo
        or message.video
        or message.voice
    ):
        message.caption = "" if not message.caption else message.caption
        caption = "" if not message.caption else message.caption_html_urled
        return caption, True
    else:
        return "", False


def send_edited_message(
    bot: Bot, message: TMessage, dest_message_id: int, chat_id: int, quote: bool
):
    """Edit the message at destination message ID of given chat."""
    from_tag = (
        Message.ENTITY_FROM.format(
            USER_ID=message.from_user.id,
            FULL_NAME=message.from_user.full_name,
        )
        if quote
        else ""
    )
    text, caption, send_from = _get_quotable(message, from_tag)
    media = _get_media(message, caption)

    if caption:
        try:
            bot.edit_message_caption(
                chat_id=chat_id, message_id=dest_message_id, caption=caption
            )
        except:
            pass

    if message.location:
        try:
            bot.edit_message_live_location(
                chat_id=chat_id, message_id=dest_message_id, location=message.location
            )
        except:
            pass

    if media:
        try:
            bot.edit_message_media(
                chat_id=chat_id, message_id=dest_message_id, media=media
            )
        except:
            pass

    if text:
        try:
            bot.edit_message_text(
                chat_id=chat_id, message_id=dest_message_id, text=text
            )
        except:
            pass

    if send_from:
        msg = bot.send_message(
            chat_id=chat_id,
            text=from_tag,
            reply_to_message_id=dest_message_id,
        )
        return msg.message_id


def send_message(
    bot: Bot,
    message: TMessage,
    to_user: int,
    reply_to: int,
    anonymous: bool,
    quote: bool,
):
    """Send message to given user after proper quotation."""
    from_tag = _get_from_tag(message, quote) if not anonymous else ""
    text, caption, send_from = _get_quotable(message, from_tag)
    msg: TMessage = None
    msgs = []

    if text:
        msg = bot.send_message(
            chat_id=to_user,
            text=text,
            reply_to_message_id=reply_to,
        )
    elif caption:
        msg = message.copy(
            chat_id=to_user,
            caption=caption,
            reply_to_message_id=reply_to,
        )
    else:
        msg = message.copy(
            chat_id=to_user,
            reply_to_message_id=reply_to,
        )

    msgs.append(msg.message_id)

    if send_from and not anonymous:
        omsg = bot.send_message(
            chat_id=to_user,
            text=from_tag,
            reply_to_message_id=msg.message_id,
        )
        msgs.append(omsg.message_id)

    return msgs
