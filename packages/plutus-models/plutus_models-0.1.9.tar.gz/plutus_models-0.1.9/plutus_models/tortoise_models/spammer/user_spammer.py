from tortoise import Model, fields


class UsersSpammer(Model):
    id = fields.BigIntField(pk=True)
    status = fields.BooleanField(default=None, null=True)
    user = fields.ForeignKeyField(
        "plutus.User",
        on_delete=fields.SET_NULL,
        null=True)
    spammer = fields.ForeignKeyField(
        "plutus.Spammer",
        on_delete=fields.SET_NULL,
        null=True)
    bot = fields.ForeignKeyField(
        "plutus.Bot",
        on_delete=fields.SET_NULL,
        null=True)

    action = fields.ForeignKeyField(
        "plutus.Action",
        on_delete=fields.SET_NULL,
        null=True)

    class Meta:
        table = "users_spammer"
