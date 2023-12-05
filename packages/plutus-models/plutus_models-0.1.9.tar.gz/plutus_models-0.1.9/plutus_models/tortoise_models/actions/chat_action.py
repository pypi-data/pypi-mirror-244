from enum import Enum

from tortoise import Model, fields


class ChatAction(Model):
    """
    Model to tell the user that something is going on the bot's side.
    The status is set for 5 seconds or less
        (when a message arrives from your bot, Telegram clients clear its typing status)
    """
    class Actions(str, Enum):
        TYPING = "Typing"
        UPLOAD_PHOTO = "Upload photo"
        UPLOAD_VIDEO = "Upload video"
        RECORD_VIDEO = "Record video"
        UPLOAD_VOICE = "Upload voice"
        RECORD_VOICE = "Record voice"
        UPLOAD_DOCUMENT = "Upload document"
        UPLOAD_VIDEO_NOTE = "Upload video note "
        RECORD_VIDEO_NOTE = "Record video note"

    chat_action = fields.CharEnumField(Actions)

    duration = fields.IntField(default=5)

    class Meta:
        table = "chat_action"
