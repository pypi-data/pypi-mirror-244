from tortoise import Model, fields


class FileModel(Model):
    """File model."""
    id = fields.BigIntField(pk=True)
    message = fields.ForeignKeyField(
        "plutus.MessageModel", on_delete=fields.SET_NULL, null=True)
    path = fields.CharField(max_length=250)
    content_type = fields.CharField(max_length=50)

    def __str__(self):
        return self.path

    class Meta:
        table = "file"
