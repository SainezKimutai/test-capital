from django.conf import settings


class ReplenishmentEntry(object):

    def __init__(self, request):
        self.session = request.session
        replenishment_entry = self.session.get(settings.REPLENISHMENT_SESSION_ID)
        if not replenishment_entry:
            replenishment_entry = self.session[settings.REPLENISHMENT_SESSION_ID] = {
                'new_entry': True,
                'supplier_id': None,
                'delivery_number': 0000,
                'items': [],
                'added_items': [],
                'removed_items': []
            }
        self.replenishment_entry = replenishment_entry

    def add(self, item=None):
        if item:
            if self.replenishment_entry['new_entry']:
                self.replenishment_entry['items'].append(item)
            else:
                self.replenishment_entry['added_items'].append(item)
        self.save()

    def save(self):
        self.session[settings.REPLENISHMENT_SESSION_ID] = self.replenishment_entry
        self.session.modified = True

    def update(self, replenishment=None, item=None, new_entry=None):
        if new_entry is not None:
            self.replenishment_entry['new_entry'] = new_entry
        if replenishment:
            if 'supplier_id' in replenishment:
                self.replenishment_entry['supplier_id'] = replenishment['supplier_id']
            if 'delivery_number' in replenishment:
                self.replenishment_entry['delivery_number'] = replenishment['delivery_number']
            if 'id' in replenishment:
                self.replenishment_entry['id'] = replenishment['id']
        if item:
            for index, value in enumerate(self.replenishment_entry['items']):
                if value['id'] == item['id']:
                    self.replenishment_entry['items'][index]['inventory_id'] = int(item['inventory_id'])
                    self.replenishment_entry['items'][index]['count'] = item['count']
                    self.replenishment_entry['items'][index]['amount'] = item['amount']
                    break
        self.save()

    def remove(self, item_id):

        for index, value in enumerate(self.replenishment_entry['items']):
            if value['id'] == item_id:
                if not self.replenishment_entry['new_entry']:
                    self.replenishment_entry['removed_items'].append(
                        self.replenishment_entry['items'][index]
                    )
                del self.replenishment_entry['items'][index]
                break
        self.save()

    def clear(self):
        del self.session[settings.REPLENISHMENT_SESSION_ID]
        self.session.modified = True
