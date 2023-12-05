from tortoise import fields, Model


class Chats(Model):
    """Chats model."""
    id = fields.BigIntField(pk=True)
    bot_id = fields.BigIntField()
    chat_id = fields.BigIntField()
    user = fields.ForeignKeyField(
        "plutus.User", on_delete=fields.CASCADE)
    updated_at = fields.DatetimeField()

    def __str__(self):
        return f"Dialogue (bot {self.bot_id} chat{self.chat_id})"

    class Meta:
        table = "chats"
        ordering = ['-updated_at']
