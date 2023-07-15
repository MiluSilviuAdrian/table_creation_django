from django.db import models
from django.core.exceptions import ValidationError

def validate_field_type(value):
    allowed_types = ['string', 'number', 'boolean']
    if value not in allowed_types:
        raise ValidationError(f"Invalid field type: {value}. Allowed types are {', '.join(allowed_types)}")

class Table(models.Model):
    fields = models.JSONField()

    def create_model(self):
        attrs = {
            '__module__': __name__,
            'id': models.AutoField(primary_key=True),
            '__str__': lambda self: str(self.id),
        }

        for field in self.fields:
            field_name = field['name']
            field_type = field['type']
            field_instance = self.get_model_field(field_type)
            attrs[field_name] = field_instance

        return type(self.__class__.__name__ + 'Model', (models.Model,), attrs)

    @staticmethod
    def get_model_field(field_type):
        if field_type == 'string':
            return models.CharField(max_length=255)
        elif field_type == 'number':
            return models.DecimalField(max_digits=10, decimal_places=2)
        elif field_type == 'boolean':
            return models.BooleanField()
        else:
            raise ValidationError(f"Invalid field type: {field_type}")

class TableRow(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='rows')
    data = models.JSONField()