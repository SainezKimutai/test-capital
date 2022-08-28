from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.http import require_POST

from base.addcart import Cart
from base.models.inventory import Inventory


class POSView(View):

    def get(self, request):
        context = dict()
        data_items = dict()
        inventories = Inventory.objects.all()
        cart = Cart(request)

        for item in cart:
            item['update_quantity_form'] = {'quantity': item['quantity'], 'update': True}
            item['update_price_form'] = {'price': item['price'], 'update': True}
            item['is_wholesale'] = item['is_wholesale']
        for inventory in inventories:
            data_items.setdefault(inventory.category.name, []).append(inventory)

        context['data'] = data_items
        context['cart'] = cart
        template_name = 'pos/pos.html'
        return render(request, template_name, context)


# Add to cart views
def cart_add(request, id):
    cart = Cart(request)
    inventory = get_object_or_404(Inventory, id=id)
    cart.add(inventory=inventory, quantity=1, price=inventory.selling_price, update_quantity=True)
    return redirect('pos_view')


# Remove Shopping Cart views
def cart_remove(request, id):
    cart = Cart(request)
    inventory = get_object_or_404(Inventory, id=id)
    cart.remove(inventory)
    return redirect('pos_view')


# update Shopping Cart views
@require_POST
def cart_updated(request, id):
    number = None
    cart = Cart(request)
    if request.method == 'POST':
        number = request.POST.get('number', None)
        price = request.POST.get('price', None)

    inventory = get_object_or_404(Inventory, id=id)
    if number:
        # Validate, quantity does not exceed stock available
        if inventory.current_stock < int(number):
            messages.add_message(request, messages.ERROR,
                                 f'Current stock is {inventory.current_stock} which is less than {int(number)}')
            return redirect('pos_view')
        cart.add(inventory=inventory, quantity=int(number), update_quantity=True)

    # Validate, modified price is not less than minimum_selling_price
    if price:
        if int(price) < inventory.min_selling_price:
            messages.add_message(request, messages.ERROR,
                                 f'Price should not be below: KES {inventory.min_selling_price}')
            return redirect('pos_view')
        cart.add(inventory=inventory, price=int(price), update_price=True)

    return redirect('pos_view')


def pos_inventory_search(request):
    inventories = Inventory.objects.all()
    query = request.GET.get('q')
    context = dict()
    data_items = dict()
    if query:
        inventories = Inventory.objects.filter(
            Q(short_description__icontains=query) |
            Q(full_description__icontains=query) |
            Q(name__icontains=query) |
            Q(range__name__icontains=query) |
            Q(color__name__icontains=query) |
            Q(finish__name__icontains=query) |
            Q(size__value=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        )

    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] = {'quantity': item['quantity'], 'update': True}

    for inventory in inventories:
        data_items.setdefault(inventory.category.name, []).append(inventory)

    context['data'] = data_items
    context['cart'] = cart
    context['query'] = query

    return render(request, 'pos/pos.html', context)
