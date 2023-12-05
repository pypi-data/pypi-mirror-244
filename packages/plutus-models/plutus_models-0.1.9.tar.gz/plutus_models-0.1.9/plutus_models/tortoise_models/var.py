from tortoise import Model, fields


class Var(Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    var = fields.CharField(max_length=64)
    value = fields.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.var

    class Meta:
        table = "var"
