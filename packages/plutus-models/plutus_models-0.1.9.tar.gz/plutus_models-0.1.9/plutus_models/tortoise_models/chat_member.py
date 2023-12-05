from tortoise import Model, fields


class ChatMember(Model):
    id = fields.BigIntField(pk=True)
    chat_uid = fields.BigIntField()
    user = fields.ForeignKeyField(
        "plutus.User", on_delete=fields.SET_NULL, null=True)
    bot = fields.ForeignKeyField(
        "plutus.Bot", on_delete=fields.SET_NULL, null=True)
    checked = fields.BooleanField(default=False)
    is_request = fields.BooleanField(default=False)
    approved = fields.BooleanField(default=False)

    def __str__(self):
        return self.user

    class Meta:
        table = "chat_member"
        unique_together = ("chat_uid", "user", "bot")
