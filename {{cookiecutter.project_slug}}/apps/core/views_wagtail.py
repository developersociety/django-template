import os

from django.apps import apps
from django.contrib.admin.utils import unquote
from django.core.paginator import Paginator
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.template import TemplateDoesNotExist, loader
from django.urls import reverse
from django.views.decorators.csrf import requires_csrf_token

from sentry_sdk import last_event_id
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.search.backends import get_search_backend
from wagtail.search.index import class_is_indexed

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


def choose(request, app, model):
    model = apps.get_model(app, model)
    items = model.objects.all()

    # Search
    is_searchable = class_is_indexed(model)
    is_searching = False

    # Creation
    create_link = reverse(
        "{app_label}_{model_name}_modeladmin_create".format(
            app_label=model._meta.app_label, model_name=model._meta.model_name
        )
    )

    search_query = None
    if is_searchable and "q" in request.GET:
        search_form = SearchForm(
            request.GET, placeholder="Search {}".format(model._meta.verbose_name_plural)
        )

        if search_form.is_valid():
            search_query = search_form.cleaned_data["q"]

            search_backend = get_search_backend()
            items = search_backend.search(search_query, items)
            is_searching = True

    else:
        search_form = SearchForm(placeholder="Search {}".format(model._meta.verbose_name_plural))

    # Pagination
    paginator = Paginator(items, per_page=25)
    paginated_items = paginator.page(request.GET.get("p", 1))

    # If paginating or searching, render 'results.html'
    if request.GET.get("results", None) == "true":
        return render(
            request,
            "wagtailadmin/widgets/model_chooser_results.html",
            {
                "model_opts": model._meta,
                "items": paginated_items,
                "query_string": search_query,
                "is_searching": is_searching,
                "create_link": create_link,
            },
        )

    return render_modal_workflow(
        request,
        "wagtailadmin/widgets/choose.html",
        None,
        {
            "model_opts": model._meta,
            "items": paginated_items,
            "is_searchable": is_searchable,
            "search_form": search_form,
            "query_string": search_query,
            "is_searching": is_searching,
            "create_link": create_link,
        },
        json_data={"step": "choose"},
    )


def chosen(request, app, model, pk):
    model = apps.get_model(app, model)
    item = get_object_or_404(model, pk=unquote(pk))

    edit_link = reverse(
        "{app_label}_{model_name}_modeladmin_edit".format(
            app_label=model._meta.app_label, model_name=model._meta.model_name
        ),
        kwargs={"instance_pk": item.pk},
    )

    model_data = {"id": str(item.pk), "string": str(item), "edit_link": edit_link}

    return render_modal_workflow(
        request, None, None, None, json_data={"step": "chosen", "result": model_data}
    )
