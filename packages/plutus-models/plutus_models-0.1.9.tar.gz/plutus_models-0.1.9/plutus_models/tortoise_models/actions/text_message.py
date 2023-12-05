from tortoise import fields

from .base import BaseParameters, TextABC


class TextMessage(BaseParameters, TextABC):
    """
    Model to send text messages
    """

    disable_web_page_preview = fields.BooleanField(default=False)

    class Meta:
        table = "text_message"
