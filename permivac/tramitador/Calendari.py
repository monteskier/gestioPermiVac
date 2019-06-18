from .models import Calendari, Treballadors
import datetime, calendar

class Cal:
    #diu a la vista si el usuari disposa de calendari per poder gravar els canvis al ell.
    def __init__(self):
        pass
    def exist(self, pk):
        try:
            print("El codi del treballador es:"+str(pk))
            traballdor = Treballadors.objects.get(id=pk)
            calendari = Calendari.objects.filter(treballador__id=pk).filter(any=datetime.date.today().year)
            return True
        except Calendari.DoesNotExist:
            return False
    #afegeix a calandari, els dies triats al tipus corresponent

    def recompte(self, data_sol):
        dies = data_sol.split(";")
        print("Dies de la sol despres de split ';' :'"+str(dies))
        intervals = data_sol.split("/")
        print("Dies en intervals despres de split '/': "+str(intervals))
        cont = 0;
        for dia in dies:
            intervals = dia.split("/")
            if(len(intervals) > 1):
                print("primer:"+intervals[0]+"_segon:"+intervals[1])
                primer = datetime.datetime.strptime((intervals[0]),'%Y-%m-%d').date()
                segon = datetime.datetime.strptime((intervals[1]),'%Y-%m-%d').date()
                delta = segon - primer
                cont = cont + delta.days
            else:
                cont=cont+1
        print("Total de dies: %s" %cont)
        return(cont)
        print("En total s'han demanat %s dies" % cont)

    def gravar(self, pk, tipus, dies, data_sol):
        try:
            calendari = Calendari.objects.get(treballador__id=pk, any=datetime.date.today().year)
            if(tipus=="vacances"):
                calendari.vacances = calendari.vacances - dies
                calendari.vacances_dies = calendari.vacances_dies + data_sol;
                calendari.save()

            elif(tipus=="perm_precep"):
                calendari.perm_precep = calendari.perm_precep + dies
                calendari.perm_precep_dies = calendari.perm_precep_dies + data_sol
                calendari.save()

            elif(tipus=="perm_no_precep"):
                calendari.perm_no_precep = calendari.perm_no_precep + dies
                calendari.perm_no_precep_dies = calendari.perm_no_precep_dies + data_sol
                calendari.save()

            elif(tipus=="asum_p"):
                calendari.asum_p = calendari.asum_p - dies
                calendari.asum_p_dies = calendari.asum_p_dies + data_sol
                calendari.save()

        except Calendari.DoesNotExist:
            return False
