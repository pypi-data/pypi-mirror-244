from tortoise import Model, fields


class Spammer(Model):
    title = fields.CharField(max_length=64)
    group_bots = fields.ManyToManyField(
        "plutus.GroupBot", through='spammer_group_bots')
    bots = fields.ManyToManyField(
        "plutus.Bot", through='spammer_bots')
    blocks = fields.ManyToManyField("plutus.Block", through='spammer_blocks')
    action = fields.ForeignKeyField("plutus.Action", on_delete=fields.SET_NULL, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    date_from = fields.DatetimeField(editable=True, blank=True)
    date_to = fields.DatetimeField(editable=True, blank=True)
    is_running = fields.BooleanField(default=False)
    is_finished = fields.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        table = "spammer"
