from tortoise import Model, fields


class ReplyButton(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    text = fields.CharField(max_length=32)

    go_to_new_line = fields.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        table = "reply_button"
