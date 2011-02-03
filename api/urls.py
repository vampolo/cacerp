from django.conf.urls.defaults import *
from piston.resource import Resource
from cacerp.api.handlers import *

persona_handler = Resource(PersonaHandler)
lettera_handler = Resource(LetteraHandler)
chiamata_handler = Resource(ChiamataHandler)

urlpatterns = patterns('',
   url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/'}, name='api'),
   url(r'^Persona\.(?P<emitter_format>.+)$', persona_handler),
   url(r'^Persona/(?P<id>\d+).(?P<emitter_format>.+)$', persona_handler),
   url(r'^Lettera\.(?P<emitter_format>.+)$', lettera_handler),
   url(r'^Chiamata\.(?P<emitter_format>.+)$', chiamata_handler),
   url(r'^lists/clienti\.(?P<emitter_format>.+)$', Resource(ListClientiHandler)),
   url(r'^lists/portatori\.(?P<emitter_format>.+)$', Resource(ListPortatoriHandler)),
   url(r'^lists/portatori/venuti\.(?P<emitter_format>.+)$', Resource(ListPortatoriVenuti)),
   url(r'^lists/potenziali\.(?P<emitter_format>.+)$', Resource(ListPotenziali)),
   url(r'^lists/potenziali/venuti\.(?P<emitter_format>.+)$', Resource(ListPotenzialiVenuti)),
   url(r'^search/Persona\.(?P<emitter_format>.+)$', 'callcenter.views.search'),
)