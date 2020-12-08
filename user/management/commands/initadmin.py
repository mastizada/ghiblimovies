from django.conf import settings
from django.core.management import BaseCommand, CommandError

from user.models import User


class Command(BaseCommand):
    help = "Create a superuser with a provided password if it doesn't exist."

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        if not all([settings.DEFAULT_ADMIN_USERNAME, settings.DEFAULT_ADMIN_EMAIL, settings.DEFAULT_ADMIN_PASS]):
            raise CommandError("Default admin details are not set!")

        if User.objects.filter(username=settings.DEFAULT_ADMIN_USERNAME).exists():
            return

        User.objects.create_superuser(
            username=settings.DEFAULT_ADMIN_USERNAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=settings.DEFAULT_ADMIN_PASS,
        )
