from django.core.management.base import BaseCommand
from home.models import Industry, Categories, SubCategories
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Update industry slugs'

    def handle(self, *args, **kwargs):
        industryes = Industry.objects.all()
        for industry in industryes:
            industry.slug = slugify(industry.name)
            industry.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated slug for "{industry.name}"'))

        categories = Categories.objects.all()
        for categori in categories:
            categori.slug = slugify(categori.name)
            categori.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated slug for "{categori.name}"'))
        
        sub_categories = SubCategories.objects.all()
        for sub_cate in sub_categories:
            sub_cate.slug = slugify(sub_cate.name)
            sub_cate.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated slug for "{sub_cate.name}"'))