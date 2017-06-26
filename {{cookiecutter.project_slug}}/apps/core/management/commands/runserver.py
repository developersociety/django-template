import atexit
import os
import subprocess

from django.contrib.staticfiles.management.commands.runserver import (
    Command as StaticfilesRunserverCommand
)


class Command(StaticfilesRunserverCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            '--nogulp',
            action='store_false',
            dest='use_gulp',
            default=True,
            help='Tells Django to NOT start gulp.'
        )

    def run(self, **options):
        if options.get('use_gulp'):
            self.set_gulp_environment_variables()
            self.start_gulp(**options)

        super().run(**options)

    def set_gulp_environment_variables(self):
        # Only set environment variables on the outer process
        outer_process = 'RUN_MAIN' not in os.environ

        if outer_process:
            os.environ['DJANGO_IP'] = self.addr
            os.environ['DJANGO_PORT'] = self.port

            # Now move Django to another port
            os.environ['BROWSERSYNC_PORT'] = str(int(self.port) + 1)

    def start_gulp(self, **options):
        inner_process = 'RUN_MAIN' in os.environ
        use_reloader = options.get('use_reloader')

        # Don't start gulp on the inner process with autoreload
        if inner_process and use_reloader:
            return

        gulp_args = []

        # Only be noisy if verbosity >= 1
        if options.get('verbosity') < 1:
            gulp_args.append('--silent')

        if gulp_args:
            gulp_args = ['--'] + gulp_args

        self.stdout.write('>>> Starting gulp')
        self.gulp_process = subprocess.Popen(
            ['npm', 'start'] + gulp_args,
            shell=False,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )
        self.stdout.write('>>> gulp process on pid {}'.format(self.gulp_process.pid))

        def kill_gulp_process():
            self.stdout.write('>>> Closing gulp process')
            self.gulp_process.terminate()
            self.gulp_process.wait()

        atexit.register(kill_gulp_process)
