from tortoise import Model, fields


class Dialogue(Model):
    title = fields.CharField(max_length=64)

    start_block = fields.ForeignKeyField("plutus.Block", on_delete=fields.SET_NULL, null=True)

    class Meta:
        table = "dialogue"

    def __str__(self):
        return self.title
