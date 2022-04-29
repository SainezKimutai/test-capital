from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.http import require_POST

from base.addcart import Cart
from base.models.product import Product


class POSView(View):

    def get(self, request):
        context = dict()
        data_items = dict()
        products = Product.objects.all()
        cart = Cart(request)

        for item in cart:
            item['update_quantity_form'] = {'quantity': item['quantity'], 'update': True}

        for product in products:
            data_items.setdefault(product.product_category.name, []).append(product)

        context['data'] = data_items
        context['cart'] = cart
        template_name = 'pos/pos.html'
        return render(request, template_name, context)


# Add to cart views
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product, quantity=1, update_quantity=1)
    return redirect('pos_view')


# Remove Shopping Cart views
def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('pos_view')


# update Shopping Cart views
@require_POST
def cart_updated(request, id):
    number = None
    cart = Cart(request)
    if request.method == 'POST':
        number = int(request.POST.get('number'))
    product = get_object_or_404(Product, id=id)
    cart.add(product=product, quantity=number, update_quantity=True)
    return redirect('pos_view')
