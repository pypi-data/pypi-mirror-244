from enum import Enum

from tortoise.models import Model
from tortoise import fields


class Partner(str, Enum):
    UNKNOWN = "UNKNOWN"
    ONE_WIN = "1WIN"
    GLORY = "GLORY"


class Category(str, Enum):
    """
    Postbacks provided by 1win
    """
    UNKNOWN = "UNKNOWN"
    REGISTRATION = "REG"
    DEPOSIT = "DEP"
    FIRST_DEPOSIT = "FDEP"
    REVENUE = "REV"


class Postback(Model):
    id = fields.IntField(pk=True)
    partner = fields.CharEnumField(Partner, default=Partner.UNKNOWN)
    category = fields.CharEnumField(Category, max_length=10, default=Category.UNKNOWN)
    created_at = fields.DatetimeField()
    user_id = fields.BigIntField()
    amount = fields.FloatField(null=True)
    sub1 = fields.TextField(null=True, description="Telegram uid")
    sub2 = fields.TextField(null=True, description="Link")
    sub3 = fields.TextField(null=True, description="Telegram bot uid")
    sub4 = fields.TextField(null=True)
    sub5 = fields.TextField(null=True, description="Project name")

    class Meta:
        table = "postback"
        table_description = "Webhook from partner"
        ordering = ["id"]

    def __str__(self):
        return str(self.user_id)
