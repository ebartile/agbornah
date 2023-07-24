from django.core.management.base import BaseCommand
from users.models import User
from users.views import user_register

class Command(BaseCommand):
    help = 'Creates dummy users'

    def handle(self, *args, **kwargs):

        user_register(username="agbornah23", password="agbornah")
        user_register(username="agbornah24", password="agbornah")
        print("Success")