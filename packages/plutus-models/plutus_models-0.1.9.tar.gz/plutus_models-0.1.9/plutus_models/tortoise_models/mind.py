from tortoise import Model, fields


class Mind(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    title = fields.CharField(max_length=64)

    f_filter = fields.ForeignKeyField("plutus.Filter", on_delete=fields.SET_NULL, null=True, related_name="minds")

    action = fields.ForeignKeyField("plutus.Action", on_delete=fields.SET_NULL, null=True, related_name="minds")

    def __str__(self):
        return self.title

    class Meta:
        table = "mind"
