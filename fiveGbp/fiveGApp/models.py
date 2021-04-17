from django.db import models
import pymongo

# ------------------------------------------------------------------------------

class RunScenariosModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    nameInScript = models.CharField(max_length=100, null=False, blank=True)
    availability = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Scenario'
        verbose_name_plural = 'Scenarios'

    def __str__(self):
        return self.name
