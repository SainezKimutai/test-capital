from django.urls import path

from base.views.auth_view import LogoutView, UserLoginView
from base.views.category_view import (
    CategoryCreateView, CategoryDeleteView, CategoryListView,
    CategoryUpdateView, category_search
)
from base.views.color_view import (
    ColorCreateView, ColorDeleteView, ColorListView, ColorUpdateView,
    color_search
)
from base.views.customer_view import (
    CreateCustomerView, CustomerDeleteView, CustomerDetailView,
    CustomerListView, CustomerUpdateView, customer_search
)
from base.views.damaged_inventory_view import (
    DamagedInventoryCreateView, DamagedInventoryDeleteView,
    DamagedInventoryListView, DamagedInventoryUpdateView,
    damaged_inventory_search
)
from base.views.dashboard_view import Dashboard
from base.views.expense_view import (
    CreateExpenseView, ExpenseDetailView, ExpenseListView, ExpenseUpdateView,
    expense_search
)
from base.views.finish_view import (
    FinishCreateView, FinishDeleteView, FinishListView, FinishUpdateView,
    finish_search
)
from base.views.inventory_view import (
    CreateInventoryView, InventoryDeleteView, InventoryDetailView,
    InventoryListView, InventoryUpdateView, inventory_search
)
from base.views.order_views import OrderItemView, bulling_information_view
from base.views.pos_view import POSView, cart_add, cart_remove, cart_updated
from base.views.product_view import CreateProductView, ProductListView
from base.views.promotion_view import (
    PromotionCreateView, PromotionDeleteView, PromotionListView,
    PromotionUpdateView, promotion_search
)
from base.views.range_view import (
    RangeCreateView, RangeDeleteView, RangeListView, RangeUpdateView,
    range_search
)
from base.views.replenishment_view import (
    ReplenishmentCreateView, ReplenishmentDeleteView, ReplenishmentListView,
    replenishment_search
)
from base.views.size_view import (
    SizeCreateView, SizeDeleteView, SizeListView, SizeUpdateView, size_search
)
from base.views.supplier_view import (
    CreateSupplierView, SupplierDeleteView, SupplierDetailView,
    SupplierListView, SupplierUpdateView, supplier_search
)
from base.views.tag_view import (
    TagCreateView, TagDeleteView, TagListView, TagUpdateView, tag_search
)

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
    path('category-search/', category_search, name='category_search'),

    path('color-create/', ColorCreateView.as_view(), name='color_create'),
    path('color/', ColorListView.as_view(), name='color_list'),
    path('color/<pk>/', ColorUpdateView.as_view(), name='color_update'),
    path('color-delete/<pk>/', ColorDeleteView.as_view(), name='color_delete'),
    path('color-search/', color_search, name='color_search'),

    path('size-create/', SizeCreateView.as_view(), name='size_create'),
    path('size/', SizeListView.as_view(), name='size_list'),
    path('size/<pk>/', SizeUpdateView.as_view(), name='size_update'),
    path('size-delete/<pk>/', SizeDeleteView.as_view(), name='size_delete'),
    path('size-search/', size_search, name='size_search'),

    path('tag-create/', TagCreateView.as_view(), name='tag_create'),
    path('tag/', TagListView.as_view(), name='tag_list'),
    path('tag/<pk>/', TagUpdateView.as_view(), name='tag_update'),
    path('tag-delete/<pk>/', TagDeleteView.as_view(), name='tag_delete'),
    path('tag-search/', tag_search, name='tag_search'),

    path('range-create/', RangeCreateView.as_view(), name='range_create'),
    path('range/', RangeListView.as_view(), name='range_list'),
    path('range/<pk>/', RangeUpdateView.as_view(), name='range_update'),
    path('range-delete/<pk>/', RangeDeleteView.as_view(), name='range_delete'),
    path('range-search/', range_search, name='range_search'),

    path('finish-create/', FinishCreateView.as_view(), name='finish_create'),
    path('finish/', FinishListView.as_view(), name='finish_list'),
    path('finish/<pk>/', FinishUpdateView.as_view(), name='finish_update'),
    path('finish-delete/<pk>/', FinishDeleteView.as_view(), name='finish_delete'),
    path('finish-search/', finish_search, name='finish_search'),

    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
    path('inventory/<pk>/', InventoryDetailView.as_view(), name='inventory_detail'),
    path('inventory-update/<pk>/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory-delete/<pk>/', InventoryDeleteView.as_view(), name='inventory_delete'),
    path('inventory-search/', inventory_search, name='inventory_search'),

    path('create-product/', CreateProductView.as_view(), name='product_create'),
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('cart/<int:id>/', cart_add, name='cart_add'),
    path('cart-update/<int:id>/', cart_updated, name='cart_updated'),
    path('cart-remove/<int:id>/', cart_remove, name='cart_remove'),
    path('pos/', POSView.as_view(), name='pos_view'),
    path('bulling-infromation/', bulling_information_view, name='bulling_information'),
    path('order-infromation/', OrderItemView.as_view(), name='order_information'),
    path('create-supplier/', CreateSupplierView.as_view(), name='supplier_create'),
    path('supplier/', SupplierListView.as_view(), name='supplier_list'),
    path('supplier/<pk>/', SupplierDetailView.as_view(), name='supplier_detail'),
    path('supplier-update/<pk>/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('supplier-delete/<pk>/', SupplierDeleteView.as_view(), name='supplier_delete'),
    path('supplier-search/', supplier_search, name='supplier_search'),
    path('create-customer/', CreateCustomerView.as_view(), name='customer_create'),
    path('customer/', CustomerListView.as_view(), name='customer_list'),
    path('customer/<pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customer-update/<pk>/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customer-delete/<pk>/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('customer-search/', customer_search, name='customer_search'),
    path('create-expense/', CreateExpenseView.as_view(), name='expense_create'),
    path('expense/', ExpenseListView.as_view(), name='expense_list'),
    path('expense/<pk>/', ExpenseDetailView.as_view(), name='expense_detail'),
    path('expense-update/<pk>/', ExpenseUpdateView.as_view(), name='expense_update'),
    path('expense-search/', expense_search, name='expense_search'),
    path('replenishment-create/', ReplenishmentCreateView.as_view(), name='replenishment_create'),
    path('replenishment/', ReplenishmentListView.as_view(), name='replenishment_list'),
    path('replenishment-delete/<pk>/', ReplenishmentDeleteView.as_view(), name='replenishment_delete'),
    path('replenishment-search/', replenishment_search, name='replenishment_search'),
    path('promotion-create/', PromotionCreateView.as_view(), name='promotion_create'),
    path('promotion/', PromotionListView.as_view(), name='promotion_list'),
    path('promotion-update/<pk>/', PromotionUpdateView.as_view(), name='promotion_update'),
    path('promotion-delete/<pk>/', PromotionDeleteView.as_view(), name='promotion_delete'),
    path('promotion-search/', promotion_search, name='promotion_search'),
    path('damaged-inventory-create/', DamagedInventoryCreateView.as_view(), name='damaged_inventory_create'),
    path('damaged-inventory/', DamagedInventoryListView.as_view(), name='damaged_inventory_list'),
    path('damaged-inventory-update/<pk>/', DamagedInventoryUpdateView.as_view(), name='damaged_inventory_update'),
    path('damaged-inventory-delete/<pk>/', DamagedInventoryDeleteView.as_view(), name='damaged_inventory_delete'),
    path('damaged-inventory-search/', damaged_inventory_search, name='damaged_inventory_search'),
]
