from tortoise import fields
from tortoise.models import Model


class RemoteIdentity(Model):
    id = fields.IntField(pk=True)
    key_id = fields.CharField(max_length=512, unique=True)
    controller = fields.CharField(max_length=512)
    public_key = fields.CharField(max_length=1024)
