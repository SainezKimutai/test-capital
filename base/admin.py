from django.contrib import admin

from base.models.category import Category
from base.models.inventory import Inventory
from base.models.tag import Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'created', 'modified']
    list_display_links = ['name', 'parent']
    list_filter = ['name']
    list_per_page = 8


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)


class InventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'current_stock', 'recent_buying_price', 'selling_price',
                    'min_selling_price']
    list_display_links = ['name', 'category']
    list_editable = ['current_stock', 'recent_buying_price', 'selling_price', 'min_selling_price']
    list_filter = ['name', 'current_stock']
    search_fields = ['name']
    list_per_page = 8


admin.site.register(Inventory, InventoryAdmin)
