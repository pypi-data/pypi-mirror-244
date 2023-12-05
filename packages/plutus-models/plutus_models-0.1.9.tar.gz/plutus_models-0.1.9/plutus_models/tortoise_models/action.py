from tortoise import Model, fields


class Action(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    title = fields.CharField(max_length=64)

    text_message = fields.ForeignKeyField("plutus.TextMessage", on_delete=fields.SET_NULL, null=True)

    photo_message = fields.ForeignKeyField("plutus.PhotoMessage", on_delete=fields.SET_NULL, null=True)

    audio_message = fields.ForeignKeyField("plutus.AudioMessage", on_delete=fields.SET_NULL, null=True)

    document_message = fields.ForeignKeyField("plutus.DocumentMessage", on_delete=fields.SET_NULL, null=True)

    video_message = fields.ForeignKeyField("plutus.VideoMessage", on_delete=fields.SET_NULL, null=True)

    animation_message = fields.ForeignKeyField("plutus.AnimationMessage", on_delete=fields.SET_NULL, null=True)

    voice_message = fields.ForeignKeyField("plutus.VoiceMessage", on_delete=fields.SET_NULL, null=True)

    video_note_message = fields.ForeignKeyField("plutus.VideoNoteMessage", on_delete=fields.SET_NULL, null=True)

    media_group_message = fields.ForeignKeyField("plutus.MediaGroupMessage", on_delete=fields.SET_NULL, null=True)

    chat_action = fields.ForeignKeyField("plutus.ChatAction", on_delete=fields.SET_NULL, null=True)

    approve_request = fields.ForeignKeyField("plutus.ApproveRequest", on_delete=fields.SET_NULL, null=True)

    http_request_action = fields.ForeignKeyField(
        "plutus.HttpRequestAction",
        on_delete=fields.SET_NULL,
        null=True
    )

    reply_buttons = fields.ManyToManyField("plutus.ReplyButton", through="action_reply_buttons")

    inline_buttons = fields.ManyToManyField("plutus.InlineButton", through="action_inline_buttons")

    remove_reply_buttons = fields.BooleanField(default=False)

    event = fields.ForeignKeyField("plutus.Event", on_delete=fields.SET_NULL, null=True)

    mind = fields.ForeignKeyField("plutus.Mind", on_delete=fields.SET_NULL, null=True, related_name="action_mind")

    block = fields.ForeignKeyField("plutus.Block", on_delete=fields.SET_NULL, null=True)

    none_object = fields.ForeignKeyField("plutus.NoneObject", on_delete=fields.SET_NULL, null=True)

    class Meta:
        table = "action"

    def __str__(self):
        return self.title
