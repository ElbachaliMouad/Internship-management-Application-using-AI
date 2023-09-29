from django.utils import timezone
from stagiaire.models import Offre
from background_task import background

@background(schedule=60, repeat=60) 
def update_expired_offers():
    now = timezone.now()
    expired_offers = Offre.objects.filter(date_of_expiry__gte=now, valable=1)

    for offer in expired_offers:
        offer.valable = 0
        offer.stagiaire_set.filter(status__in=[1, 2]).update(status=0)
        offer.save()


update_expired_offers()