from django.forms.fields import CharField

from .validators import ProhibitNullCharactersValidator

# Make CharField form field prohibit null characters
CharField.default_validators.append(ProhibitNullCharactersValidator())
