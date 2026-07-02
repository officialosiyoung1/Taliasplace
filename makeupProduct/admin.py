from django.contrib import admin
from .models import MakeupProduct
@admin.register(MakeupProduct)

class MakeupProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'quantity', 'colour', 'price', 'owner')
    search_fields = ('name', 'brand', 'colour')
    list_filter = ('brand', 'colour')

# Register your models here.
