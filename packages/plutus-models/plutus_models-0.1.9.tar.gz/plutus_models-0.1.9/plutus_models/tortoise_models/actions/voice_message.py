from .base import BaseParameters, MediaABC, TextABC, ThumbnailABC


class VoiceMessage(BaseParameters, MediaABC, TextABC):
    """
    Model to send audio files, if you want Telegram clients to display the file as a playable voice message
    """
    class Meta:
        table = "voice_message"
