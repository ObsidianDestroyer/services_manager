from tortoise import fields
from tortoise.models import Model


class Service(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, unique=True)
    status = fields.BooleanField(default=False)
    locked = fields.BooleanField(default=False)

    def render(self) -> dict:
        return {
            'serviceID': self.id,
            'serviceName': self.name,
            'serviceStatus': self.status,
            'serviceLock': self.locked,
        }
