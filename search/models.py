from django.db import models
# Create your models here.
class Collect(models.Model):
    error_id = models.CharField(max_length=20)
    error_type = models.CharField(max_length=200, null=True, blank=True)
    error_index = models.CharField(max_length=2000, null=True, blank=True)
    def __str__(self):
        return self.error_type