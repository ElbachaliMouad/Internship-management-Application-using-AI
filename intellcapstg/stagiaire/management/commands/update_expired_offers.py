from django.core.management.base import BaseCommand
from stagiaire.task import update_expired_offers

class Command(BaseCommand):
    help = 'Update expired offers every 60 seconds'

    def handle(self, *args, **kwargs):
        # Call the task and set it to repeat every 60 seconds
        update_expired_offers()