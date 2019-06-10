from .models import Calendari, Treballadors
import datetime

class Cal():
    def get(pk):
        try:
            print("El codi del treballador es:"+str(pk))
            traballdor = Treballadors.objects.get(id=pk)
            calendari = Calendari.objects.filter(treballador__id=pk).filter(any=datetime.date.today().year)
            return True
        except Calendari.DoesNotExist:
            return False
