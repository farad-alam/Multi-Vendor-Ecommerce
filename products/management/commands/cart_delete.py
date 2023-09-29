
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import ProgrammingError

class Command(BaseCommand):
    help = 'Delete specified database tables'

    def add_arguments(self, parser):
        parser.add_argument('tables', nargs='+', type=str, help='Table names to delete')

    def handle(self, *args, **options):
        tables = options['tables']
        with connection.cursor() as cursor:
            for table in tables:
                try:
                    cursor.execute(f'DROP TABLE IF EXISTS {table}')
                    self.stdout.write(self.style.SUCCESS(f'Successfully deleted table: {table}'))
                except ProgrammingError as e:
                    self.stdout.write(self.style.ERROR(f'Error deleting table: {table}\n{str(e)}'))
