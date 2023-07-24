from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Deletes in active users'

    def handle(self, *args, **kwargs):
        users = User.objects.filter(is_active=False)
        users.delete()
        print("Success")