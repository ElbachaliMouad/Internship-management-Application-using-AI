from django.utils import timezone
from .models import Offre
from background_task import background

def update_expired_offers():
    now = timezone.now()
    expired_offers = Offre.objects.filter(date_of_expiry__lt=now, valable=1)

    for offer in expired_offers:
        offer.valable = 0
        offer.stagiaire_set.filter(status__in=[1, 2]).update(status=0)
        offer.save()

@background(schedule=60)  # Schedule to run every 60 seconds (adjust as needed)
def schedule_update_expired_offers():
    update_expired_offers()