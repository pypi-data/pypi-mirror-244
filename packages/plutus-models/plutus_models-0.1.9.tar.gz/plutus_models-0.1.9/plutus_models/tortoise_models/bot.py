from tortoise import Model, fields


class Bot(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=64)
    uid = fields.BigIntField(null=False)
    token = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)

    dialog = fields.ForeignKeyField("plutus.Dialogue", on_delete=fields.SET_NULL, null=True)

    vars = fields.ManyToManyField("plutus.Var", through="bot_vars")

    enable = fields.BooleanField(default=True)

    trigger_on_start = fields.BooleanField(default=True)
    trigger_on_join_request = fields.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        table = "bot"
