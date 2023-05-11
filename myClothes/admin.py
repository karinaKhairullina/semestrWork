from django.contrib import admin
from .models import Category, Subcategory, Image, ClothingItem

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Image)
admin.site.register(ClothingItem)