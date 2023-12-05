from tortoise import fields

from .base import BaseParameters


class MediaGroupMessage(BaseParameters):
    """
    Model to send a group of photos, videos, documents or audios as an album.
    Documents and audio files can be only grouped in an album with messages of the same type.
    """

    photos = fields.ManyToManyField(
        "plutus.PhotoMessage", through="media_group_message_photos",
        backward_key="mediagroupmessage_id", forward_key="photomessage_id")

    videos = fields.ManyToManyField(
        "plutus.VideoMessage", through="media_group_message_videos",
        backward_key="mediagroupmessage_id", forward_key="videomessage_id")

    documents = fields.ManyToManyField(
        "plutus.DocumentMessage", through="media_group_message_documents",
        backward_key="mediagroupmessage_id", forward_key="documentmessage_id")

    audios = fields.ManyToManyField(
        "plutus.AudioMessage", through="media_group_message_audios",
        backward_key="mediagroupmessage_id", forward_key="audiomessage_id")

    class Meta:
        table = "media_group_message"
