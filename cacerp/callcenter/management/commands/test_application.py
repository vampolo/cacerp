from django.core.management.base import BaseCommand, CommandError
from sys import stdout
from inspect import getmembers, getargs
from callcenter.models import *
import callcenter.views
import datetime
from api.handlers import *



class Command(BaseCommand):
    def test_run_all(self):
        for name, value in getmembers(self):
            if name.startswith("test") and not name.startswith('test_run_all') and len(getargs(value.func_code)[0][1:]) == 0 and value.__doc__ != 'deprecated':
                print 'Running: '+ name
                value()
                print ''
            
        
        
    def handle(self, *args, **options):
        if len (args) == 0:
            stdout.write("\n".join(([ str((name,  getargs(value.func_code)[0][1:])) for name, value in getmembers(self) if name.startswith("test")])))
            stdout.write("\n")
        else:
            getattr(self, args[0])(*args[1:])
            
    
    def test_add_fields(self):
        persone = add_fields_to_persona(Persona.objects.filter(cliente = True))
        for persona in persone:
            print persona.__dict__

    def test_etichette(self):
        callcenter.views.genEtichette({'TEST':True})
        
    def change_for_letters(self):
        p_list = Persona.objects.filter(note__icontains='GEN11')
        for p in p_list:
            l = Lettera(persona=p, data=datetime.now(), status=False)
            l.save()