import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from base.models.category import Category
from base.models.tag import Tag
from base.models.color import Color
from base.models.size import Size
from base.models.range import Range
from base.models.finish import Finish
from base.models.customer import Customer
from base.models.expense import Expense
from base.models.supplier import Supplier
from django_seed import Seed

User = get_user_model()
seeder = Seed.seeder()


class Command(BaseCommand):
    help = 'Seed Database'

    def generate_phone_numbers(self):
        return f"+2547{random.randint(10, 99)}{random.randint(100, 999)}{random.randint(100, 999)}",

    def handle(self, *args, **options):  # noqa
        self.seed_database()

        self.stdout.write(
            self.style.SUCCESS('Database Successfully seeded'))

    def seed_database(self):
        # Foreign keys must be seeded first
        seeder.add_entity(User, 5)
        seeder.add_entity(Category, 5)
        seeder.add_entity(Tag, 5)
        seeder.add_entity(Color, 5)
        seeder.add_entity(Size, 5)
        seeder.add_entity(Range, 5)
        seeder.add_entity(Finish, 5)
        seeder.add_entity(Customer, 10, {
            'phone_number': lambda x: f"+2547{random.randint(10, 99)}{random.randint(100, 999)}{random.randint(100, 999)}",
            'email': lambda x: seeder.faker.email(),
        })
        seeder.add_entity(Supplier, 10, {
            'phone_number_1': lambda x: f"+2547{random.randint(10, 99)}{random.randint(100, 999)}{random.randint(100, 999)}",
            'email': lambda x: seeder.faker.email(),
        })
        seeder.add_entity(Expense, 3)

        seeder.execute()
