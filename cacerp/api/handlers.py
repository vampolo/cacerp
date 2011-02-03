from piston.handler import BaseHandler
from piston.forms import ModelForm
from piston.utils import rc
from callcenter.models import *
from django.core.exceptions import *


#stupid piston doesn't send the id of the model, this makes all working
BaseHandler.exclude = ()
            
class PersonaHandler(BaseHandler):
    model = Persona
    form = PersonaForm
    
    def has_form(self):
        return hasattr(self, 'form')
    
    def flatten_dict(self, dct):
        return dict([(str(k), dct.get(k)) for k in dct.keys() if dct.get(k) != ''])
        
    def update(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        pkfield = self.model._meta.pk.name

        if pkfield not in kwargs:
            # No pk was specified
            return rc.BAD_REQUEST

        try:
            inst = Persona.objects.get(pk=kwargs.get(pkfield))
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        except MultipleObjectsReturned: # should never happen, since we're using a PK
            return rc.BAD_REQUEST
        
        if self.has_form():
            forminst = self.form(request.POST, instance=inst)
            forminst.save()
        else:
            attrs = self.flatten_dict(request.data)
            for k,v in attrs.iteritems():
                setattr( inst, k, v )

            inst.save()
            
        return rc.ALL_OK
    
    def create(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        attrs = self.flatten_dict(request.POST)

        try:
            inst = Persona.objects.get(**attrs)
            return rc.DUPLICATE_ENTRY
        except self.model.DoesNotExist:
            if self.has_form():
                forminst = self.form(request.POST)
                inst = forminst.save()
            else:
                inst = self.model(**attrs)
                inst.save()
            return inst
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY
        
class LetteraHandler(BaseHandler):
    model = Lettera
    
    
class ChiamataHandler(BaseHandler):
    model = Chiamata
    form = ChiamataForm
    
    def has_form(self):
        return hasattr(self, 'form')
    
    def flatten_dict(self, dct):
        return dict([(str(k), dct.get(k)) for k in dct.keys() if dct.get(k) != ''])
    
    def create(self, request, *args, **kwargs):
            if self.has_form():
                forminst = self.form(request.POST)
                inst = forminst.save()
            return inst
        
class ListClientiHandler(BaseHandler):
    def read(self, request):
        return Persona.objects.filter(cliente = True)

class ListPortatoriHandler(BaseHandler):
    def read(self, request):
        return Persona.objects.filter(cliente = False, porta_apparecchio = True, venuto = False)
    
class ListPortatoriVenuti(BaseHandler):
    def read(self, request):
        return Persona.objects.filter(cliente = False, problemi_udito = True, porta_apparecchio = True, venuto = True)

class ListPotenziali(BaseHandler):
    def read(self, request):
        return Persona.objects.filter(cliente = False, problemi_udito = True, venuto = False)

class ListPotenzialiVenuti(BaseHandler):
    def read(self, request):
        return Persona.objects.filter(cliente = False, problemi_udito = True, venuto = True)

class SearchPersona(BaseHandler):
    def read(self, request):
        p = Persona.objects.all()
        if request.GET.get('nome',''):
            p = p.filter(nome__icontains=request.GET.get('nome',''))
        if request.GET.get('cognome',''):
            p = p.filter(cognome__icontains=request.GET.get('cognome',''))
        if request.GET.get('secondo_cognome',''):
            p = p.filter(secondo_cognome__icontains=request.GET.get('secondo_cognome',''))
        if request.GET.get('indirizzo',''):
            p = p.filter(indirizzo__icontains=request.GET.get('indirizzo',''))
        if request.GET.get('numero_civico',''):
            p = p.filter(numero_civico__icontains=request.GET.get('numero_civico',''))
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
        if request.GET.get('cliente',''):
            p = p.filter(cliente=True)
        if request.GET.get('problemi_udito',''):
            p = p.filter(problemi_udito=True)
        if request.GET.get('porta_apparecchio',''):
            p = p.filter(porta_apparecchio=True)
        if request.GET.get('venuto',''):
            p = p.filter(venuto=True)
        if request.GET.get('spontaneo',''):
            p = p.filter(spontaneo=True)
        if request.GET.get('perdita_media',''):
            p = p.filter(perdita_media__icontains=request.GET.get('perdita_media',''))
        if request.GET.get('note',''):
            p = p.filter(note__icontains=request.GET.get('note',''))
        if request.GET.get('preventivo',''):
            p = p.filter(preventivo_media__icontains=request.GET.get('preventivo',''))
        
        start = int(request.GET.get('start', 0))
        limit = int(request.GET.get('limit', len(p)))
        
        return json.dumps({"totalCount": len(p),"root": [pe.__dict__ for pe in p[start:limit]]})
        