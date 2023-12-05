from enum import Enum

from tortoise import Model, fields


class ApproveRequest(Model):
    """
    The model is responsible for accepting to join the channel.
    """
    class Quantity(str, Enum):
        FIRST = "First"
        ALL = "All"

    quantity = fields.CharEnumField(Quantity)

    class Meta:
        table = "approve_request"
