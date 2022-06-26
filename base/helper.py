

def generate_receipt(model_name, receipt_prefix):
    """
        Generates an incremented receipt number based on individual model
        Example: 'INV0003'

        Params:
            model_name: Pass the db model, eg Invoice
            receipt_prefix: Pass any string that uniquely identifies the
            number from other models number. eg 'INV'
    """
    last_item = model_name.objects.all().order_by('id').last()
    if not last_item:
        return f'{receipt_prefix}0001'
    item_receipt_number = last_item.receipt_number
    receipt_int = int(item_receipt_number.split(receipt_prefix)[-1])
    new_receipt_int = receipt_int + 1
    new_receipt_no = receipt_prefix + str(new_receipt_int).zfill(4)
    return new_receipt_no


def clean_file_to_array(csv_string):
    """
        This methods returns csv row in an array;
        i.e [['header_1', 'header_2'], ['value_1', 'value_2']]
    """
    new_string = []
    for line in csv_string.splitlines():
        if line.strip():
            new_string.append(line.replace('"', '').split(","))
    return new_string


bulk_edit_headers = [
    'id',
    'name',
    'color__name',
    'range__name',
    'category__name',
    'finish__name',
    'size__value',
    'current_stock',
    'recent_buying_price',
    'max_selling_price',
    'min_selling_price',
    'selling_price',
    'wholesale_price',
    'wholesale_minimum_number'
]
