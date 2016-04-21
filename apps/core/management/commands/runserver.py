# -*- coding: utf-8 -*-

import atexit
import os
import signal
import subprocess

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import (
    Command as StaticfilesRunserverCommand
)


class Command(StaticfilesRunserverCommand):

    def inner_run(self, *args, **options):
        self.start_grunt()
        return super(Command, self).inner_run(*args, **options)

    def start_grunt(self):
        self.stdout.write('>>> Starting grunt')
        self.grunt_process = subprocess.Popen(
            ['node_modules/.bin/grunt --gruntfile={0}/gruntfile.js --base=.'.format(
                os.path.join(settings.BASE_DIR)
            )],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )

        self.stdout.write(
            '>>> Grunt process on pid {0}'.format(self.grunt_process.pid)
        )

        def kill_grunt_process(pid):
            self.stdout.write('>>> Closing grunt process')
            os.kill(pid, signal.SIGTERM)

        atexit.register(kill_grunt_process, self.grunt_process.pid)
