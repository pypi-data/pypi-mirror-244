from tortoise import Model, fields


class GroupBot(Model):
    id = fields.BigIntField(pk=True)
    title = fields.CharField(max_length=64)
    bot = fields.ManyToManyField(
        "plutus.Bot", through='group_bot_bots',
        backward_key='groupbot_id', related_name='groupbots')

    def __str__(self):
        return self.title

    class Meta:
        table = "group_bot"