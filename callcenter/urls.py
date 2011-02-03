from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'callcenter.views.index', name='callcenter'),
    (r'^ultimePersoneChiamate$', 'callcenter.views.ultimePersoneChiamate'),
    (r'^Chiamate/?(?P<id>.*)$', 'callcenter.views.Chiamate'),
    (r'^LetterePersone$', 'callcenter.views.LetterePersone'),
    (r'^generaEtichette$', 'callcenter.views.genEtichette'),
    (r'^sendLetter/?(?P<id>[0-9]+)$', 'callcenter.views.sendLetter'),
    (r'^lettersSent$', 'callcenter.views.lettersSent'),
)
