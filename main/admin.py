from django.contrib import admin
from unicodedata import category

from .models import Category, Product

# admin.site.register

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug'] # Параметри які є в моделі які будуть відображатись в самій адмінці
    prepopulated_fields = {'slug': ('name',)} # Поля які ми автоматично заповнюємо

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'description', 'available', 'image', 'created', 'updated']
    list_filter = ['created', 'updated', 'available', 'category'] # Дозволить фільтрувати за даними факторами
    list_editable = ['category', 'price', 'available']
    prepopulated_fields = {'slug': ('name',)}  # Поля які ми автоматично заповнюємо

