import atexit
import os
import signal
import subprocess

from django.contrib.staticfiles.management.commands.runserver import \
    Command as StaticfilesRunserverCommand


class Command(StaticfilesRunserverCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            '--nogrunt',
            action='store_false',
            dest='use_grunt',
            default=True,
            help='Tells Django to NOT start grunt.'
        )

    def run(self, **options):
        if options.get('use_grunt'):
            self.start_grunt(**options)

        super().run(**options)

    def start_grunt(self, **options):
        inner_process = 'RUN_MAIN' in os.environ
        use_reloader = options.get('use_reloader')

        # Don't start grunt on the inner process with autoreload
        if inner_process and use_reloader:
            return

        self.stdout.write('>>> Starting grunt')
        self.grunt_process = subprocess.Popen(
            ['npm', 'start'],
            shell=False,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )

        self.stdout.write('>>> Grunt process on pid {0}'.format(self.grunt_process.pid))

        def kill_grunt_process(pid):
            self.stdout.write('>>> Closing grunt process')
            os.kill(pid, signal.SIGTERM)

        atexit.register(kill_grunt_process, self.grunt_process.pid)
