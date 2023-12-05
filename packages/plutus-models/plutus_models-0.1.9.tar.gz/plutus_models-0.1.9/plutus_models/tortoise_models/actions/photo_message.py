from .base import BaseParameters, MediaABC, TextABC


class PhotoMessage(BaseParameters, MediaABC, TextABC):
    """
    Model to send photos
    """

    class Meta:
        table = "photo_message"
