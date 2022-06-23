import datetime
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from base.models.inventory import Inventory
from base.models.promotion import Promotion


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, inventory, quantity=1, price=1, update_quantity=False, update_price=False):
        inventory_id = str(inventory.id)
        if inventory_id not in self.cart:
            self.cart[inventory_id] = {'quantity': 0, 'price': str(inventory.selling_price)}

        if update_quantity:
            self.cart[inventory_id]['quantity'] = quantity

        if update_price:
            self.cart[inventory_id]['price'] = price

        if self.cart[inventory_id]['quantity'] > inventory.wholesale_minimum_number:
            self.cart[inventory_id]['is_wholesale'] = True
            self.cart[inventory_id]['price'] = inventory.wholesale_price
        else:
            self.cart[inventory_id]['is_wholesale'] = False
            # Caters for when the quantity changes from wholesale to less than wholesale minimum number
            # Revert to selling price
            if not update_price:
                self.cart[inventory_id]['price'] = inventory.selling_price

        # Check if there is an active promotion for inventory
        current_date = datetime.date.today()

        try:
            # Assumes only one promotion for an inventory can be active at one time
            promotion = Promotion.objects.get(
                Q(inventory=inventory) &
                Q(promotion_start_date__lte=current_date) &
                Q(promotion_end_date__gte=current_date)
            )
        except ObjectDoesNotExist:
            promotion = False
            self.cart[inventory_id]['is_promotion'] = False

        if promotion:
            self.cart[inventory_id]['price'] = promotion.promotion_price
            # If a product is on promotion, use promotion price
            self.cart[inventory_id]['is_wholesale'] = False
            self.cart[inventory_id]['is_promotion'] = True

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
