from django.urls import path

from base.views.auth_view import LogoutView, UserLoginView
from base.views.category_view import (
    CategoryCreateView, CategoryDeleteView, CategoryListView,
    CategoryUpdateView
)
from base.views.customer_view import (
    CreateCustomerView, CustomerDeleteView, CustomerDetailView,
    CustomerListView, CustomerUpdateView, customer_search
)
from base.views.dashboard_view import Dashboard
from base.views.expense_view import (
    CreateExpenseView, ExpenseDetailView, ExpenseListView, ExpenseUpdateView,
    expense_search
)
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
from base.views.supplier_view import (
    CreateSupplierView, SupplierDeleteView, SupplierDetailView,
    SupplierListView, SupplierUpdateView, supplier_search
)
from base.views.tag_view import CreateListTagView, TagDeleteView, UpdateTagView

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('create-category/', CategoryCreateView.as_view(), name='create_category'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category-delete/<pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('create-inventory/', CreateInventoryView.as_view(), name='inventory_create'),
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
]
