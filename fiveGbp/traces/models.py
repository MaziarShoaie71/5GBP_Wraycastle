from django.db import models

# Create your models here.
class GeneratedTracesModel(models.Model):
    id = models.AutoField(primary_key=True)
    TestName = models.CharField(max_length=50, unique=True)
    realFileName = models.CharField(max_length=50)
    scenarioName = models.CharField(max_length=100, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Generated Trace'
        verbose_name_plural = 'Generated Traces'
    def __str__(self):
        return self.TestName
