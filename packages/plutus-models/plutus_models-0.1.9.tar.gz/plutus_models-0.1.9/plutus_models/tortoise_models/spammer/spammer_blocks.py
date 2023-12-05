from tortoise import Model, fields


class SpammerBlocks(Model):
    id = fields.BigIntField(pk=True)
    spammer_id = fields.BigIntField()
    block_id = fields.BigIntField()

    class Meta:
        table = "spammer_blocks"
