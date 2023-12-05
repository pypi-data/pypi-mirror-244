from tortoise import Model, fields


class HttpRequestAction(Model):
    """Http request action."""
    id = fields.BigIntField(pk=True)
    url = fields.CharField(
        max_length=250, description="url_string")

    class Meta:
        table = "http_request"
