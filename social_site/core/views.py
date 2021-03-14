from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404 ,render
from django.views.generic.list import ListView  #usata per la lista utenti


from forum.models import Sezione


# Create your views here.

# def homepage(request):
#     return render(request, 'core/homepage.html')


class HomeView(ListView):
    #uso queryset invece di model, mi permette di usare anche filtri e fare ordinamento
    queryset = Sezione.objects.all()
    template_name = "core/homepage.html"
    context_object_name = "lista_sezioni"   #sostituisce object_list, cioè la variabile ritornata dalla ListView


class UserList(ListView):
    model = User
    template_name = "core/users.html"
    

def user_profile_view(request, username): #gli passo l'identificativo dello user (uso la chiave primaria)
    user = get_object_or_404(User, username=username)   #prendo lo user che ha quella chiave primaria, se non esiste ottengo 404
    context = {"user": user}
    return render(request, "core/user_profile.html", context)




