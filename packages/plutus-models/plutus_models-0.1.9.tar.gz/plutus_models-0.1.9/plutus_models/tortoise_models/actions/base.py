from tortoise import Model, fields


class BaseParameters(Model):
    """
    Abstract model of basic parameters
    """
    title = fields.CharField(max_length=128)
    changed_at = fields.DatetimeField(auto_now=True)
    pin = fields.BooleanField(default=False)
    disable_notification = fields.BooleanField(default=False)
    protect_content = fields.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class MediaABC(Model):
    """
    Abstract model for adding a file
    """
    file = fields.CharField(max_length=100)

    class Meta:
        abstract = True


class TextABC(Model):
    """
    Abstract model for specifying text
    """
    text = fields.TextField(max_length=1024, null=True)

    class Meta:
        abstract = True


class ThumbnailABC(Model):
    """
    Abstract model for adding a thumbnail
    """
    thumbnail = fields.CharField(max_length=100)

    class Meta:
        abstract = True
