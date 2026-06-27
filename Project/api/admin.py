from django.contrib import admin
from .models import BioData

# Register your models here.
@admin.register(BioData)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name','age','city']