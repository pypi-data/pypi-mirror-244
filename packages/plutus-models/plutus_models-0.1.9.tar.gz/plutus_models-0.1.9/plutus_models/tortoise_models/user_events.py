from tortoise import Model, fields


class UserEvent(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    event_id = fields.BigIntField(max_length=32, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_events"
