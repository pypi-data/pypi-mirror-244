from .base import BaseParameters, MediaABC, TextABC, ThumbnailABC


class AnimationMessage(BaseParameters, MediaABC, TextABC, ThumbnailABC):
    """
    Model to send animation files (GIF or H.264/MPEG-4 AVC video without sound)
    """

    class Meta:
        table = "animation_message"
