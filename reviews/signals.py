from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from .models import Review
from accounts.models import ServiceProviderProfile,CustomUser


@receiver(post_save, sender=Review)
def update_provider_rating(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        provider = ServiceProviderProfile.objects.get(
            user=instance.provider.user
        )

        reviews = Review.objects.filter(
            provider=instance.provider
        )

        avg_rating = reviews.aggregate(
            Avg('rating')
        )['rating__avg']

        provider.average_rating = round(
            avg_rating,
            1
        )

        provider.total_reviews = reviews.count()

        provider.save()