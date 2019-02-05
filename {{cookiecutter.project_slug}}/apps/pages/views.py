from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.generic import View


class LanguageRedirectView(View):

    def get(self, request):
        language = translation.get_language_from_request(request)
        return HttpResponseRedirect('/{}/'.format(language))
