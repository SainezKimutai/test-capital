from decimal import Decimal

from django.conf import settings

from base.models.inventory import Inventory


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, inventory, quantity=1, price=1, update_quantity=False, update_price=False, wholesale_quantity=0,
            wholesale_price=0):
        inventory_id = str(inventory.id)
        if inventory_id not in self.cart:
            self.cart[inventory_id] = {'quantity': 0, 'price': str(inventory.selling_price)}

        if update_quantity:
            self.cart[inventory_id]['quantity'] = quantity

        if update_price:
            self.cart[inventory_id]['price'] = price

        self.cart[inventory_id]['is_wholesale'] = False
        if self.cart[inventory_id]['quantity'] > wholesale_quantity:
            self.cart[inventory_id]['is_wholesale'] = True
            self.cart[inventory_id]['price'] = wholesale_price

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, inventory):
        inventory_id = str(inventory.id)
        if inventory_id in self.cart:
            del self.cart[inventory_id]
            self.save()

    def __iter__(self):
        inventory_ids = self.cart.keys()
        inventories = Inventory.objects.filter(id__in=inventory_ids)
        for inventory in inventories:
            self.cart[str(inventory.id)]['inventory'] = inventory

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
