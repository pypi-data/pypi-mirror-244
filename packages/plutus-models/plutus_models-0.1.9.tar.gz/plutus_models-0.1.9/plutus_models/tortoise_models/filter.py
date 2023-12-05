from tortoise import Model, fields


class Filter(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    title = fields.CharField(max_length=64)

    chat_member = fields.BooleanField(default=False)

    registration = fields.BooleanField(default=False)

    min_first_deposit = fields.FloatField(null=True)
    max_first_deposit = fields.FloatField(null=True)

    min_sum_deposits = fields.FloatField(null=True)
    max_sum_deposits = fields.FloatField(null=True)

    negative_mind = fields.ForeignKeyField(
        "plutus.Mind", on_delete=fields.SET_NULL, null=True, related_name="negative_mind")

    neutral_mind = fields.ForeignKeyField(
        "plutus.Mind", on_delete=fields.SET_NULL, null=True, related_name="neutral_mind")

    positive_mind = fields.ForeignKeyField(
        "plutus.Mind", on_delete=fields.SET_NULL, null=True, related_name="positive_mind")

    def __str__(self):
        return self.title

    class Meta:
        table = "filter"
