from django.core.management.base import BaseCommand

from scraper.scraper import get_records


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_records()