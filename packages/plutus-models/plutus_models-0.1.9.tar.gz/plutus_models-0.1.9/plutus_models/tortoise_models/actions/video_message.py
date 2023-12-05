from .base import BaseParameters, MediaABC, TextABC, ThumbnailABC


class VideoMessage(BaseParameters, MediaABC, TextABC, ThumbnailABC):
    """
    Model to send video files
    """

    class Meta:
        table = "video_message"
