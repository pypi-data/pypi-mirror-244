from tortoise import Model, fields


class NoneObject(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    title = fields.CharField(max_length=64)

    def __str__(self):
        return self.title

    class Meta:
        table = "none_object"
