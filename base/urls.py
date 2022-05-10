from django.urls import path

from base.views.auth_view import LogoutView, UserLoginView
from base.views.category_view import (
    CategoryCreateView, CategoryDeleteView, CategoryListView,
    CategoryUpdateView
)
from base.views.dashboard_view import Dashboard
from base.views.inventory_view import (
    CreateInventoryView, InventoryDeleteView, InventoryDetailView,
    InventoryListView, InventoryUpdateView
)
from base.views.order_views import OrderItemView, bulling_information_view
from base.views.pos_view import POSView, cart_add, cart_remove, cart_updated
from base.views.product_view import CreateProductView, ProductListView
from base.views.range_view import (
    CreateListRangeView, RangeDeleteView, UpdateRangeView
)
from base.views.color_view import (
    ColorCreateView, ColorListView, ColorUpdateView, ColorDeleteView
)
from base.views.size_view import (
    SizeCreateView, SizeListView, SizeUpdateView, SizeDeleteView
)
from base.views.tag_view import CreateListTagView, TagDeleteView, UpdateTagView

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('create-inventory/', CreateInventoryView.as_view(), name='inventory_create'),

    # Configurations
    path('category-create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category-delete/<pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    path('color-create/', ColorCreateView.as_view(), name='color_create'),
    path('color/', ColorListView.as_view(), name='color_list'),
    path('color/<pk>/', ColorUpdateView.as_view(), name='color_update'),
    path('color-delete/<pk>/', ColorDeleteView.as_view(), name='color_delete'),

    path('size-create/', SizeCreateView.as_view(), name='size_create'),
    path('size/', SizeListView.as_view(), name='size_list'),
    path('size/<pk>/', SizeUpdateView.as_view(), name='size_update'),
    path('size-delete/<pk>/', SizeDeleteView.as_view(), name='size_delete'),

    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
    path('inventory/<pk>/', InventoryDetailView.as_view(), name='inventory_detail'),
    path('inventory-update/<pk>/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory-delete/<pk>/', InventoryDeleteView.as_view(), name='inventory_delete'),
    path('tag/', CreateListTagView.as_view(), name='create_list_tag'),
    path('tag/<pk>/', TagDeleteView.as_view(), name='tag_delete'),
    path('tag-update/<pk>/', UpdateTagView.as_view(), name='tag_update'),
    path('range/', CreateListRangeView.as_view(), name='create_list_range'),
    path('range/<pk>/', RangeDeleteView.as_view(), name='range_delete'),
    path('range-update/<pk>/', UpdateRangeView.as_view(), name='range_update'),
    path('create-product/', CreateProductView.as_view(), name='product_create'),
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('cart/<int:id>/', cart_add, name='cart_add'),
    path('cart-update/<int:id>/', cart_updated, name='cart_updated'),
    path('cart-remove/<int:id>/', cart_remove, name='cart_remove'),
    path('pos/', POSView.as_view(), name='pos_view'),
    path('bulling-infromation/', bulling_information_view, name='bulling_information'),
    path('order-infromation/', OrderItemView.as_view(), name='order_information'),
]
