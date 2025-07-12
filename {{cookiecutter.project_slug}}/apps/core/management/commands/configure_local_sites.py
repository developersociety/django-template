from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Updates Django sites hostnames/ports for local development"

    def handle(self, *args, **options):
        if settings.DEBUG is False:
            raise CommandError(
                "Command only to be used for local development (DEBUG must be True)"
            )

        self.stdout.write(self.style.NOTICE("Django sites for this project:\n"))

        port = 8000
        for site in Site.objects.order_by("id"):
            site.domain = f"127.0.0.1:{port}"
            site.save()
            self.stdout.write(f" {site.id:2d} - {site.name}")
            port += 1000

        self.stdout.write(
            self.style.NOTICE(
                "\nTo run a specific site: run SITE_ID=<site_id> ./manage.py runserver"
            )
        )
