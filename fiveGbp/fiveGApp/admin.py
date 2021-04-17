from django.contrib import admin
from fiveGApp.models import RunScenariosModel
# Register your models here.

# To add id (pk) to admin panel
class RunScenariosModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(RunScenariosModel, RunScenariosModelAdmin)
