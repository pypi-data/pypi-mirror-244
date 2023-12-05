import enum

from tortoise import Model, fields


class MessageModel(Model):
    """Telegram message model."""

    class ContentType(enum.StrEnum):
        MESSAGE = "message"
        APPROVE = "approve"
        CALLBACK = "callback"
        HTTP_REQUEST = "http_request"

    chat_id = fields.BigIntField()
    bot_id = fields.BigIntField()
    message_id = fields.BigIntField(null=True)
    json = fields.JSONField()
    is_edited = fields.BooleanField(default=False)
    is_pinned = fields.BooleanField(default=False)
    content_type = fields.CharEnumField(
        ContentType, max_length=100, default="message")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Actual message (bot{self.bot_id} chat{self.chat_id} "
            f"message{self.message_id})"
        )

    class Meta:
        table = "message"
        ordering = ['-created_at']
