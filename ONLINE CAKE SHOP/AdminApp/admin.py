from django.contrib import admin
from AdminApp.models import Category,Cake
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","cat_name")


class CakeAdmin(admin.ModelAdmin):
    list_display = ("id","cname","price","description","image_url","category")


admin.site.register(Cake,CakeAdmin)
admin.site.register(Category,CategoryAdmin)

