from django.shortcuts import redirect, render
from django.views.generic import ListView

from base.addcart import Cart
from base.forms.sales_form import SalesOrderForm
from base.models.sales import SalesItem


def make_payment_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.created_by = request.user
            order.total_amount = cart.get_total_price()
            order.modified_by = request.user
            order.save()
            for item in cart:
                inventory = item['inventory']
                SalesItem.objects.create(
                    sales_order=order,
                    inventory=inventory,
                    price=item['price'],
                    quantity=item['quantity'],
                    total_amount=item['quantity'] * item['price']
                )
                # Update inventory to reduce the count
                inventory.current_stock = inventory.current_stock - item['quantity']
                inventory.save()

            cart.clear()
        return redirect('pos_view')
    else:
        form = SalesOrderForm()
    return render(request, 'pos/sales_order_information.html', {'form': form, 'cart': cart})


class SalesItemView(ListView):
    template_name = 'pos/sales_item_list.html'
    model = SalesItem
    context_object_name = 'sales_item'
    paginate_by = 15
