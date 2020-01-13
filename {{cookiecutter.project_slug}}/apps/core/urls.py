from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^choose/$", views.choose, name="models_choose_generic"),
    url(r"^choose/(\w+)/(\w+)/$", views.choose, name="models_choose"),
    url(r"^choosen/(\w+)/(\w+)/([^/]+?)/$", views.chosen, name="models_chosen"),
]
