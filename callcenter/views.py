from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import connection
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import *
from django.core.servers.basehttp import FileWrapper
from appy.pod.renderer import Renderer
import os
from models import *

import django.utils.simplejson as simplejson
import datetime
class JSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj,datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            try:
                res = simplejson.JSONEncoder.default(self, obj)
            except TypeError:
                res = 'ERROR'
        return res

json2 = JSONEncoder()

def add_fields_to_persona(persone, *args, **kwargs):
    for persona in persone:
        try:
            call = Chiamata.objects.filter(persona = persona).latest()
        except ObjectDoesNotExist:
            continue
        persona.data_ultima_chiamata = call.data
        for k,v in risposta_choices:
            if call.risposta == k: 
                persona.risposta = v
                break
    return persone

def index(request):
    return render_to_response('callcenter_index.html')

def search(request, emitter_format):
        p = Persona.objects.all().order_by('cognome')
        if request.GET.get('nome',''):
            p = p.filter(nome__icontains=request.GET.get('nome',''))
        if request.GET.get('cognome',''):
            p = p.filter(cognome__icontains=request.GET.get('cognome',''))
        if request.GET.get('secondo_cognome',''):
            p = p.filter(secondo_cognome__icontains=request.GET.get('secondo_cognome',''))
        if request.GET.get('indirizzo',''):
            p = p.filter(indirizzo__icontains=request.GET.get('indirizzo',''))
        if request.GET.get('citta',''):
            p = p.filter(citta__icontains=request.GET.get('citta',''))
        if request.GET.get('provincia',''):
            p = p.filter(provincia__icontains=request.GET.get('provincia',''))
        if request.GET.get('cap',''):
            p = p.filter(cap__icontains=request.GET.get('cap',''))
        if request.GET.get('telefono',''):
            p = p.filter(telefono__icontains=request.GET.get('telefono',''))
        if request.GET.get('email',''):
            p = p.filter(email__icontains=request.GET.get('email',''))
        if request.GET.get('cliente') == 'on':
            p = p.filter(cliente=True)
        if request.GET.get('problemi_udito') == 'on':
            p = p.filter(problemi_udito=True)
        if request.GET.get('porta_apparecchio') == 'on':
            p = p.filter(porta_apparecchio=True)
        if request.GET.get('venuto') == 'on':
            p = p.filter(venuto=True)
        if request.GET.get('spontaneo') == 'on':
            p = p.filter(spontaneo=True)
        if request.GET.get('perdita_media',''):
            p = p.filter(perdita_media__icontains=request.GET.get('perdita_media',''))
        if request.GET.get('note',''):
            p = p.filter(note__icontains=request.GET.get('note',''))
        if request.GET.get('preventivo',''):
            p = p.filter(preventivo_media__icontains=request.GET.get('preventivo',''))
        
        start = int(request.GET.get('start', 0))
        limit = int(request.GET.get('limit', len(p)))
        
        result = p[start:start+limit]
        
        result = add_fields_to_persona(result)
        
        return HttpResponse(json2.encode({"totalCount": len(p),"root": [pe.__dict__ for pe in result]}))

def ultimePersoneChiamate(request):
    calls = Chiamata.objects.all()
    p = list()
    for c in calls:
        c.persona.data_ultima_chiamata = c.data
        p.append(c.persona) 
    
    start = int(request.GET.get('start', 0))
    limit = int(request.GET.get('limit', len(p)))
    
    return HttpResponse(json2.encode({"totalCount": len(p),"root": [x.__dict__ for x in p[start:start+limit]]}))

def Chiamate(request, id):
    calls = Chiamata.objects.filter(persona = Persona.objects.get(pk = id)).order_by('-data')
    
    start = int(request.GET.get('start', 0))
    limit = int(request.GET.get('limit', len(calls)))
    
    for x in calls[start:start+limit]:
        x.risposta = x.get_risposta_display()
    
    return HttpResponse(json2.encode({"totalCount": len(calls),"root": [x.__dict__ for x in calls[start:start+limit]]}))

def LetterePersone(request):
    p = Lettera.objects.filter(status=False)
    
    start = int(request.GET.get('start', 0))
    limit = int(request.GET.get('limit', len(p)))
    
    res = [dict(x.__dict__,**x.persona.flat()) for x in p[start:start+limit]]
    
    return HttpResponse(json2.encode({"totalCount": len(res),"root": res }))

    
def genEtichette(request):
    
    basepath=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'etichette')
    try:     
        os.remove(os.path.join(basepath, 'etichette.odt'))
    except OSError:
        pass
    letters = Lettera.objects.filter(status=False)
    p_list = list(set(x.persona for x in letters))
    p_list.sort(key=lambda x: x.cognome)
    renderer = Renderer(os.path.join(basepath,'EtichetteA4Cac.odt'), {'p_list':p_list}, os.path.join(basepath, 'etichette.odt'))
    renderer.run()
    response = HttpResponse(FileWrapper(open(os.path.join(basepath, 'etichette.odt'))), content_type='application/vnd.oasis.opendocument.text')
    response['Content-Disposition'] = 'attachment; filename=etichette.odt'
    response['Content-Length'] = os.path.getsize(os.path.join(basepath, 'etichette.odt'))
    return response
    
def sendLetter(request, id):
    try:
        p = Persona.objects.get(pk=int(id))
    except Persona.DoesNotExist:
        return HttpResponseNotFound()
    l = Lettera(persona=p, data=datetime.date.today(), status=False)
    l.save()
    return HttpResponse(json2.encode({"totalCount": 1, 'root':l.__dict__}))

def lettersSent(request):
    for x in Lettera.objects.filter(status=False):
        x.status=True
        x.save()
    return HttpResponse(json2.encode({"totalCount": 1, 'success':True}))
    
    
    
             