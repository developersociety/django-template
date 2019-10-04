import os

from django.http import HttpResponseServerError
from django.template import TemplateDoesNotExist, loader
from django.views.decorators.csrf import requires_csrf_token

from sentry_sdk import last_event_id

ERROR_500_TEMPLATE_NAME = "500.html"


@requires_csrf_token
def server_error(request, template_name=ERROR_500_TEMPLATE_NAME):
    """
    500 error handler with request context and Sentry Event ID.
    """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        if template_name != ERROR_500_TEMPLATE_NAME:
            # Reraise if it's a missing custom template.
            raise
        return HttpResponseServerError("<h1>Server Error (500)</h1>", content_type="text/html")
    return HttpResponseServerError(
        template.render(
            {
                "request": request,
                "sentry_dsn": os.environ.get("SENTRY_DSN"),
                "sentry_event_id": last_event_id(),
            }
        )
    )
