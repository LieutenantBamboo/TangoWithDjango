from django.contrib import admin
from rango.models import Category, Page


class FlatPageAdmin(admin.ModelAdmin):
    fields = ('title','category','url')

class PersonAdmin(admin.ModelAdmin):
    fileds = ('','','')

admin.site.register(Category)
admin.site.register(Page)