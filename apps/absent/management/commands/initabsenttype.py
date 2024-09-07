from django.core.management.base import BaseCommand
from apps.absent.models import AbsentType


class Command(BaseCommand):
    def handle(self, *args, **options):
        absent_types = ['事假','病假','婚假','丧假','工伤假','产假','探亲假','公假','年休假']
        types = []
        for absent_type in absent_types:
            types.append(AbsentType(name=absent_type))
        AbsentType.objects.bulk_create(types)
        self.stdout.write(self.style.SUCCESS('Successfully created AbsentType'))
