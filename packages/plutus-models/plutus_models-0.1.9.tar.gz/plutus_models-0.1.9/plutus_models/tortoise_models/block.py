from tortoise import Model, fields


class Block(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    title = fields.CharField(max_length=64)

    events = fields.ManyToManyField("plutus.Event", through="block_events")

    def __str__(self):
        return self.title

    class Meta:
        table = "block"
