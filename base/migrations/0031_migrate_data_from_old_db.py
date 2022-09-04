# Generated by Django 3.2 on 2022-08-27 11:40

from django.db import migrations
import MySQLdb
import os
from PIL import Image
import io
from datetime import date
from django.utils.timezone import now
from django.db.models import Sum
import phonenumbers
from annoying.functions import get_object_or_None
from decimal import Decimal
from datetime import datetime
from django_seed import Seed


seeder = Seed.seeder()

db = MySQLdb.connect(host="localhost", user="capital_finishes", port=3306,
                     passwd="capital_finishes", db="kamabens_capitaldb_2022")

photos_db = MySQLdb.connect(host="localhost", user="capital_finishes", port=3306,
                            passwd="capital_finishes", db="photos_capital_db")


def get_image_from_db(p_code):
    """
    Get's image from db and saves to a folder
    Return the path
    :return:
    """
    photo_cursor = photos_db.cursor(MySQLdb.cursors.DictCursor)
    query = f"select img_photo from photos where p_code = {p_code}"
    photo_cursor.execute(query)
    data = photo_cursor.fetchall()
    if not data:
        # Exit if inventory doesn't have photo
        return False
    image = data[0]['img_photo']
    data_bytes_io = io.BytesIO(image)
    image = Image.open(data_bytes_io)
    # Create folder if it doesn't exists
    today_date = date.today()
    file_upload_dir = f'media/inventory/{today_date.year}/{today_date.month}/{today_date.day}'
    # Check whether the specified path exists or not
    path_exists = os.path.exists(file_upload_dir)

    if not path_exists:
        # Create a new directory because it does not exist
        os.makedirs(file_upload_dir)

    image_path = f"{file_upload_dir}/{p_code}.{image.format.lower()}"
    image.save(image_path)

    # Exclude media/ from string
    return image_path[6:]


def migrate_data_from_old_db(apps, schema_editor):
    try:
        cursor = db.cursor(MySQLdb.cursors.DictCursor)

        # models
        Category = apps.get_model("base", "Category")
        Range = apps.get_model("base", "Range")
        Finish = apps.get_model("base", "Finish")
        Size = apps.get_model("base", "Size")
        Color = apps.get_model("base", "Color")
        Inventory = apps.get_model("base", "Inventory")
        Customer = apps.get_model("base", "Customer")
        SalesOrder = apps.get_model("base", "SalesOrder")
        SalesItem = apps.get_model("base", "SalesItem")
        Supplier = apps.get_model("base", "Supplier")

        # Iterate through sales table records for items that are still in the system
        # select distinct(P_code) from sales_table where P_code in (select distinct(id) from new_stock)

        # Create
        query = "select * from new_stock where id in (select distinct(P_code) from sales_table " \
                "where P_code in (select distinct(id) from new_stock))"
        cursor.execute(query)
        results = cursor.fetchall()

        for record in results:
            default_data_dict = dict()
            default_data_dict['name'] = record['Description']
            default_data_dict['short_description'] = record['Description']
            default_data_dict['full_description'] = record['Description']
            default_data_dict['reorder_level'] = record['ReOrder']
            default_data_dict['recent_buying_price'] = int(record['Buying_Price'])
            default_data_dict['selling_price'] = int(record['Retail_Price'])
            default_data_dict['max_selling_price'] = int(record['Retail_Price'])
            default_data_dict['min_selling_price'] = int(record['Wholesale_Price'])
            default_data_dict['wholesale_price'] = int(record['Wholesale_Price'])
            default_data_dict['wholesale_minimum_number'] = 25
            default_data_dict['inventory_code'] = record['ID']

            # Create category
            category, category_created = Category.objects.get_or_create(name=record['Product'],
                                                                        defaults={'name': record['Product']})
            # create range
            if record['Range'] not in ['NIL', '--', 'nil', 'Nil']:
                _range, range_created = Range.objects.get_or_create(name=record['Range'],
                                                                    defaults={'name': record['Range']})
                default_data_dict['range'] = _range
            # create finish
            if record['Finish'] not in ['NIL', '--', 'nil', 'Nil']:
                finish, finish_created = Finish.objects.get_or_create(name=record['Finish'], category=category,
                                                                      defaults={'name': record['Finish'],
                                                                                'category': category})
                default_data_dict['finish'] = finish
            # create size
            if record['Size'] not in ['NIL', '--', 'nil', 'Nil']:
                size, size_created = Size.objects.get_or_create(value=record['Size'], category=category,
                                                                defaults={'value': record['Size'],
                                                                          'category': category})
                default_data_dict['size'] = size
            # create color
            if record['Colour'] not in ['NIL', '--', 'nil', 'Nil']:
                color, color_created = Color.objects.get_or_create(name=record['Colour'], category=category,
                                                                   defaults={'name': record['Colour'],
                                                                             'category': category})
                default_data_dict['color'] = color
            # create inventory
            # Get photos from photos db and save in media {model}/{year}/{month}/{day}/{file_name}
            image_path = get_image_from_db(int(record['ID']))
            if image_path:
                default_data_dict['picture'] = image_path

            # Get latest count
            query = f"select * from close_stock where Pcode = {record['ID']} order by date DESC limit 1"
            cursor.execute(query)
            results = cursor.fetchall()
            default_data_dict['current_stock'] = int(results[0]['Total'])
            default_data_dict['inventory_code'] = record['ID']
            default_data_dict['name'] = record['Description']
            default_data_dict['category'] = category

            Inventory.objects.create(**default_data_dict)
        print(f"Inventory objects created")

        # Migrate credit customers
        query = "select * from credit_customers"
        cursor.execute(query)
        results = cursor.fetchall()

        for record in results:
            Customer.objects.create(
                name=record["Business_Name"],
                is_credit=True
                )
        print(f"Customer objects created")

        # Migrate users
        User = apps.get_registered_model('auth', 'User')

        _users = [
            {"first_name": "Josephine", "last_name": "Njoroge", "user_name": "JOSEPHINE"},
            {"first_name": "Festus", "last_name": "Muhoro", "user_name": "FESTUS MUHORO"},
            {"first_name": "Timothy", "last_name": "Mwaura", "user_name": "TIMOTHY "},
            {"first_name": "Telcra", "last_name": "Njeri", "user_name": "TELCRA"},
            {"first_name": "James", "last_name": "Ngene", "user_name": "JAMES NGENE"}
        ]

        for user in _users:
            User.objects.create(
                username=user['user_name'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                email=f"{user['first_name']}@capitalfinishes.com",
                is_active=True,
                date_joined=now(),
                password='pbkdf2_sha256$260000$b7g0Jyh22xcZQz8lEpBtXd$//f7AKZGfnDfJ/MIH+WsEKcDIRZvqKndcMqEF7ZJ/rA='
                )
        print(f"User objects created")

        # Migrate sales records # sales_report
        query = "select * from sales_report where Pcode in (select distinct(id) from new_stock)"
        cursor.execute(query)
        results = cursor.fetchall()
        for record in results:
            try:
                default_data_dict = dict()
                default_data_dict['transaction_type'] = record['Sale_Type'].upper()
                default_data_dict['receipt_number'] = record['Sales_No']
                default_data_dict['sales_agent'] = User.objects.get(username='JOSEPHINE')
                sales_agent = get_object_or_None(User, username=record['User'].upper())
                if sales_agent:
                    default_data_dict['sales_agent'] = sales_agent
                if record['Sale_Type'].upper() == 'CREDIT':
                    customer, _ = Customer.objects.get_or_create(
                        name=record["Credit_Customer"],
                        defaults={'is_credit': True, 'name': record["Credit_Customer"]})
                    default_data_dict['customer'] = customer

                sales_order, _ = SalesOrder.objects.get_or_create(
                    receipt_number=record['Sales_No'],
                    defaults=default_data_dict)

                # Some records are in 24hrs others are in 12hrs
                if record['Time'][-2:].upper() in ['AM', 'PM']:
                    date_time_obj = datetime.strptime(f"{record['Datereport']} {record['Time']}", '%Y%m%y %H:%M:%S %p')
                else:
                    date_time_obj = datetime.strptime(f"{record['Datereport']} {record['Time']}", '%Y%m%y %H:%M:%S')

                sales_item_dict = dict()
                sales_item_dict['sales_order'] = sales_order
                sales_item_dict['inventory'] = Inventory.objects.get(inventory_code=str(record['Pcode']))
                sales_item_dict['price'] = record['Price']
                sales_item_dict['quantity'] = record['Quantity']
                sales_item_dict['total_amount'] = Decimal(record['Quantity'] * record['Price'])
                sales_item_dict['created'] = date_time_obj
                sales_item_dict['modified'] = date_time_obj

                SalesItem.objects.create(**sales_item_dict)
            except Exception as e:
                print(record)
                print(e)
        print(f"Sales Items and Orders objects created")

        # Populate total_amount for sales order
        for order in SalesOrder.objects.all():
            order.total_amount = SalesItem.objects.filter(
                sales_order=order).aggregate(order_total_amount=Sum('total_amount'))['order_total_amount']
            order.save()
        print(f"Sales Order totals updated")

        # Migrate Suppliers
        query = "select * from suppliers"
        cursor.execute(query)
        results = cursor.fetchall()

        for record in results:
            data_dict = dict()
            data_dict["supplier_name"] = record["Name"]
            data_dict["email"] = record["Email_Address"]

            try:
                if Supplier.objects.filter(email=record["Email_Address"]).count() > 0:
                    # Emails are quite dirty, replace with fake email if email add already exists
                    data_dict["email"] = seeder.faker.email()

                supplier_number = phonenumbers.parse(record["Telephone"], "KE")
                if Supplier.objects.filter(phone_number_1=supplier_number).count() > 0:
                    raise Exception()

                data_dict["phone_number_1"] = supplier_number
            except phonenumbers.phonenumberutil.NumberParseException:
                pass
            except Exception as e:
                print(e)
                print(record)
            finally:
                Supplier.objects.create(**data_dict)
        print(f"Supplier objects created")

        # Migrate invoices

        # Migrate credit notes
    except Exception as e:
        print(e)


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_auto_20220827_1341'),
    ]

    operations = [
        migrations.RunPython(migrate_data_from_old_db)
    ]