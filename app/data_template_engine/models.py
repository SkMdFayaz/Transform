from django.db import models
from attribute_library.models import Field

class DataTemplate(models.Model):
    name = models.CharField(max_length=255)

class FieldMapping(models.Model):
    template = models.ForeignKey(DataTemplate, on_delete=models.CASCADE, related_name='mappings')
    source_field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='source_mappings')
    destination_field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='destination_mappings')
