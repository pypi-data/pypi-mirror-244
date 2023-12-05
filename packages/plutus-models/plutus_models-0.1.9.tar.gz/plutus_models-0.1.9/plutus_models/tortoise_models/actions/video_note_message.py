from .base import BaseParameters, MediaABC, ThumbnailABC


class VideoNoteMessage(BaseParameters, MediaABC, ThumbnailABC):
    """
    Model to send video messages
    """

    class Meta:
        table = "video_note_message"
