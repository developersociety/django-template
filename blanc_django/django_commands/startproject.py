from django.core.management.commands.startproject import Command as StartCommand


class Command(StartCommand):
    def handle(self, project_name=None, target=None, *args, **options):
        # Add additional options hacked in
        options.update(self.extra_options)

        super(Command, self).handle(project_name, target, **options)
