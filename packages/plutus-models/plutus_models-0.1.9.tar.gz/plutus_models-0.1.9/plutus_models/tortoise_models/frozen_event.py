from tortoise import fields

from .user_events import UserEvent


class FrozenUserEvent(UserEvent):
    """Model that represents 'frozen' Event model when user blocks bot."""
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    event_id = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_frozen_events"
