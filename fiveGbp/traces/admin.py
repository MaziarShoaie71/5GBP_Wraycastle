from django.contrib import admin
from traces.models import GeneratedTracesModel
# Register your models here.

class GeneratedTracesModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id','created_at',)

admin.site.register(GeneratedTracesModel, GeneratedTracesModelAdmin)
