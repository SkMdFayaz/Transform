from django.db import models

class Field(models.Model):
    name = models.CharField(max_length=255)
    visible_name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name
