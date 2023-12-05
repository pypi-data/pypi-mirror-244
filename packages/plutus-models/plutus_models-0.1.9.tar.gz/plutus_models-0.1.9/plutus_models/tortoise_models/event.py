from enum import Enum

from tortoise import Model, fields


class Event(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    title = fields.CharField(max_length=64)

    """
    Joined or left the channel
    """
    class ChatMemberType(str, Enum):
        JOIN = "Join"
        LEAVE = "Leave"
        REQUEST = "Request"

    chat_member = fields.CharEnumField(ChatMemberType, null=True)

    """
    Webhook from partners
    """
    class Webhook(str, Enum):
        REG = "Registration"
        FD = "First deposit"
        DEP = "Deposit"

    webhook = fields.CharEnumField(Webhook, null=True)

    """
    Do it after a while
    """
    timer = fields.TimeDeltaField(null=True)

    """
    Message from the user
    """
    message = fields.TextField(max_length=1024, null=True)

    """
    Callback data from inline button
    """
    callback = fields.CharField(max_length=64, null=True)

    mind = fields.ForeignKeyField("plutus.Mind", on_delete=fields.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        table = "event"
