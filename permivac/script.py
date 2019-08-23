from tramitador.models import Treballadors, Calendari
from tramitador.Calendari import Cal
from permivac import settings
import datetime

def create_calendar():
    treballadors = Treballadors.objects.all()
    cal = Cal()
    today = datetime.datetime.now()
    count = 0
    for treballador in treballadors:
        try:
            calendari = Calendari.objects.get(treballador__id = treballador.id, any=today.year)
        except Calendari.DoesNotExist:
            print("No existeix cap Calendari d'aquest any al treballador")
            calendari = Calendari(any=int(today.year),vacances=22,vacances_dies=0,perm_precep=0,perm_precep_dies=0,perm_no_precep=0,perm_no_precep_dies=0,asum_p=6,asum_p_dies=0,perm_indisposicio=0,treballador=treballador)
            calendari.save()
            count = count+1;
    print("S'han creat un total de "+str(count)+" calendaris")

create_calendar()
