

from django.contrib import admin
from .models import Item, Categoria, User


# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")

class ItemAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao", "preco")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "password")
    
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(User, UserAdmin)