import atexit
import os
import subprocess

from django.core.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "--nowebpack",
            action="store_false",
            dest="use_webpack",
            default=True,
            help="Tells Django to NOT start webpack.",
        )

    def run(self, **options):
        if options.get("use_webpack"):
            self.set_webpack_environment_variables()
            self.start_webpack(**options)

        super().run(**options)

    def set_webpack_environment_variables(self):
        # Only set environment variables on the outer process
        outer_process = "RUN_MAIN" not in os.environ

        if outer_process:
            os.environ["DJANGO_IP"] = self.addr
            os.environ["DJANGO_PORT"] = self.port

            # Now move Django to another port
            os.environ["BROWSERSYNC_PORT"] = str(int(self.port) + 1)

    def start_webpack(self, **options):
        inner_process = "RUN_MAIN" in os.environ
        use_reloader = options.get("use_reloader")

        # Don"t start webpack on the inner process with autoreload
        if inner_process and use_reloader:
            return

        webpack_args = []

        # Only be noisy if verbosity >= 1
        if options.get("verbosity") < 1:
            webpack_args.append("--display=errors-only")

        if webpack_args:
            webpack_args = ["--"] + webpack_args

        self.stdout.write(">>> Starting webpack")
        self.webpack = subprocess.Popen(
            ["npm", "start"] + webpack_args,
            shell=False,
            stdin=subprocess.PIPE,
            stdout=self.stdout._out,
            stderr=self.stderr._out,
        )
        self.stdout.write(">>> Webpack process on pid {}".format(self.webpack_process.pid))

        def kill_webpack_process():
            self.stdout.write(">>> Closing webpack process")
            self.webpack_process.terminate()
            self.webpack_process.wait()

        atexit.register(kill_webpack_process)
