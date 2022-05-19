from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError

from ddf import G
from faker import Faker


class Command(BaseCommand):
    help = 'Seed the database. Run as `python manage.py seed {modelName}` e.g. python manage.py seed country. To ' \
           'see supported models, run `python manage.py seed model --list`'
    faker = Faker()

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all supported models',
        )

    def handle(self, *args, **options): # noqa
        model = options['model']
        supported_models = [
            'customer',
            'supplier',
        ]
        if options['list']:
            self.stdout.write(
                self.style.SUCCESS(
                    'The supported models are: %s' %
                    ','.join(supported_models)))
            exit()

        if model not in supported_models:
            raise CommandError('Unsupported model "%s"' % model)

        if model == 'customer':
            self.seed_customers()
        elif model == 'supplier':
            self.seed_suppliers()
        elif model == 'expenses':
            self.seed_expenses()
        else:
            raise CommandError('Unsupported model "%s"' % model)

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully seeded "%s"' %
                model))

    def seed_customers(self):
        countries = [
            "Kenya",
            "Uganda",
            "Malawi",
            "Zambia",
            "Nigeria",
            "Tanzania"]
        for country_name in countries:
            if not Country.objects.filter(name=country_name).exists():
                G(Country, name=country_name)

    def seed_suppliers(self):
        country = G(Country, name=self.faker.country())
        G(AdministrativeDivision, country=country)

    def seed_expenses(self):
        country = G(Country, name=self.faker.country())
        G(AdministrativeDivision, country=country)
