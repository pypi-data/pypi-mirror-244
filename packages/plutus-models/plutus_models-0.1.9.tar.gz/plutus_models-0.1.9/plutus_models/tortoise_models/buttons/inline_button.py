from tortoise import Model, fields


class InlineButton(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    text = fields.CharField(max_length=32)
    url = fields.CharField(max_length=200)
    callback_data = fields.CharField(max_length=64, null=True, blank=True)

    go_to_new_line = fields.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        table = "inline_button"
