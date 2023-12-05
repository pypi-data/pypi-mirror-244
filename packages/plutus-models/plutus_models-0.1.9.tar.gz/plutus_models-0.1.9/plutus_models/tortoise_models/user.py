from tortoise import Model, fields


class User(Model):
    id = fields.BigIntField(pk=True)
    uid = fields.BigIntField()
    username = fields.CharField(max_length=32, null=True)
    first_name = fields.CharField(max_length=64)
    created_at = fields.DatetimeField(auto_now_add=True)
    params = fields.TextField(max_length=64, null=True)
    status = fields.BooleanField(default=True)

    bot = fields.ForeignKeyField(
        "plutus.Bot", on_delete=fields.SET_NULL, null=True)

    block = fields.ForeignKeyField(
        "plutus.Block", on_delete=fields.SET_NULL, null=True)

    events = fields.ManyToManyField(
        "plutus.Event", through="user_events", related_name="user")
    frozen_events = fields.ManyToManyField(
        "plutus.Event", through="user_frozen_events", related_name="users")

    def __str__(self):
        return self.username

    class Meta:
        table = "user"
