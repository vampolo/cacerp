from django.db import models
from django.forms import ModelForm
from datetime import datetime

perdita_media_choices = (
    ('0%', '0%'),
    ('10%', '10%'),
    ('20%', '20%'),
    ('30%', '30%'),
    ('35%', '35%'),
    ('40%', '40%'),
    ('45%', '45%'),
    ('50%', '50%'),
    ('Oltre', 'Oltre'),
)

risposta_choices = (
    (1,'Ha risposto'),
    (2,'Assente'),
    (3,'Occupato'),
    (4,'Inesistente'),
)

pila_choices = (
                (0, 'Nessuna'),
                (1, '10'),
                (2, '312'),
                (3, '13'),
                (4, '675'),
)

lato_choices = (
                (0, 'Nessuno'),
                (1, 'Dx'),
                (2, 'Sx'),
                (3, 'Bino'),
)

class CommonObj(object):
    def __repr__(self):
        return str(self.__dict__)
    
    def __str__(self):
        return self.__repr__()
    
    def flat(self, mapping={}, func=lambda x:x, separator=' '):
        '''
            Emit a dictionary representing the class. It's able to expand the relationship between classes
            using the special __config__ class you can define in your models. When representation will occour
            it will expand the relations and will return a single field value which is the result of the join
            using the fields_separator of the main_fields list defined in __config__ for each related class.
            If the __config__ is missed it will try to use the name of the relation as the value for the emitted
            dictionary.
            
            mapping defines how to map the results. it's a dictionary composed by {existent_key:rep_key ...} which
            changes all the existent methods of the object (the existent_key) with the rep_key
        '''
        
        def get_wanted_rep(key):
            if key in mapping:
                return mapping[key]
            return key
        
        res = dict()
        iter = dict(self.__dict__)
        for k,v in iter.iteritems():
            if k[0] == '_':
                continue
            elif k[-3:] == '_id' and k != 'id':
                ist = getattr(self, k[:-3])
                if ist:
                    try:    
                        attrs = ist.__class__.__config__.main_fields
                    except AttributeError:
                        attrs = [k[:-3]]
                    
                    fields = list()
                    for attr in attrs:
                        fields.append(func(unicode(getattr(ist, attr))))
                    
                    try:
                        sep = ist.__class__.__config__.fields_separator
                        if sep:
                            separator = sep
                    except AttributeError:
                        pass
                                          
                    res[get_wanted_rep(k[:-3])] = separator.join(fields) 
            else:
                try:
                    res[get_wanted_rep(k)] = func(v)
                except AttributeError:
                    #needed to print numbers
                    res[get_wanted_rep(k)] = v
        return res

class Persona(CommonObj, models.Model):
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    secondo_cognome = models.CharField(max_length=30, blank=True, null=True)
    indirizzo = models.CharField(max_length=100, blank=True, null=True)
    citta = models.CharField(max_length=15, blank=True, null=True)
    provincia = models.CharField(max_length=30, blank=True, null=True)
    cap = models.IntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    cellulare = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cliente = models.BooleanField()
    problemi_udito = models.BooleanField()
    porta_apparecchio = models.BooleanField()
    venuto = models.BooleanField()
    spontaneo = models.BooleanField()
    perdita_media = models.CharField(max_length=5, blank=True, null=True, choices=perdita_media_choices)
    tipo_apparecchio = models.CharField(max_length=30, blank=True, null=True)
    lato_apparecchio = models.IntegerField(blank=True, null=True, choices=lato_choices)
    pila = models.IntegerField(blank=True, null=True, choices=pila_choices)
    note = models.TextField(blank=True, null=True)
    preventivo = models.TextField(blank=True, null=True)
    
class Lettera(CommonObj,models.Model):
    persona = models.ForeignKey('Persona')
    data = models.DateField()
    data_invio = models.DateField(default=None, blank=True, null=True)
    
class Chiamata(models.Model):
    persona = models.ForeignKey('Persona')
    data = models.DateTimeField(default=datetime.now, editable=False)
    risposta = models.IntegerField(blank=True, null=True, choices=risposta_choices)
    class Meta():
        ordering = ['data']
        get_latest_by = 'data'
        
class Visita(models.Model):
    persona = models.ForeignKey('Persona')
    data = models.DateTimeField()
    effettuata = models.BooleanField()
    
class PersonaForm(ModelForm):
    class Meta:
        model = Persona

class ChiamataForm(ModelForm):
    class Meta:
        model = Chiamata
