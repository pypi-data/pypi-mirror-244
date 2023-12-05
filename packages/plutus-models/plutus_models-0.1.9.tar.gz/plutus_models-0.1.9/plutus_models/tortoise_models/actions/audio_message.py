from tortoise import fields

from .base import BaseParameters, MediaABC, TextABC, ThumbnailABC


class AudioMessage(BaseParameters, MediaABC, TextABC, ThumbnailABC):
    """
    Model to send audio files
    """
    performer = fields.CharField(max_length=32)
    audio_title = fields.CharField(max_length=32)

    class Meta:
        table = "audio_message"
