import django.dispatch
from django.dispatch import receiver
from django.db import models
from .models import User


user_registered = django.dispatch.Signal() # providing_args=["user"]


@receiver(models.signals.post_save, sender=User,
          dispatch_uid="user_post_save")
def user_post_save(sender, instance, created, **kwargs):
    # ignore if object is just created
    if created:
        #sends email
        return
    
    #
