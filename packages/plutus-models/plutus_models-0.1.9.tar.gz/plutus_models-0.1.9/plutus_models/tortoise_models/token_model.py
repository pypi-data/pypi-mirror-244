from tortoise import Model, fields


class Token(Model):
    """Token model."""
    id = fields.BigIntField(pk=True)
    token = fields.UUIDField()
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "token"

    def __str__(self):
        return str(self.token)
