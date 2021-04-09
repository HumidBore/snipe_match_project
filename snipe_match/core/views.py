from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404 ,render, redirect
from django.views.generic.list import ListView  #usata per la lista utenti


from forum.models import Discussione, Post, Sezione


# Create your views here.

# def homepage(request):
#     return render(request, 'core/homepage.html')


class HomeView(ListView):
    #uso queryset invece di model, mi permette di usare anche filtri e fare ordinamento
    queryset = Sezione.objects.all()
    template_name = "core/homepage.html"
    context_object_name = "lista_sezioni"   #sostituisce object_list, cioè la variabile ritornata dalla ListView


class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = "core/users.html"
    

def user_profile_view(request, username): #gli passo l'identificativo dello user (uso la chiave primaria)
    user = get_object_or_404(User, username=username)   #prendo lo user che ha quella chiave primaria, se non esiste ottengo 404
    discussioni_utente = Discussione.objects.filter(autore_discussione=user).order_by("-pk")
    context = {"user": user, "discussioni_utente": discussioni_utente}
    return render(request, "core/user_profile.html", context)

def cerca(request):
    #controllo ci sia q, che è il nome del form dove scrivo cosa cercare
    if "q" in request.GET:
        querystring = request.GET.get("q")
        if len(querystring) == 0:   #controllo se non c'è alcun parametro di ricerca
            return redirect("/cerca/")
        #prendo tutti quelli che contengono le parole cercate (__icontains fa proprio questo)
        discussioni = Discussione.objects.filter(titolo__icontains=querystring)    
        posts = Post.objects.filter(contenuto__icontains=querystring)    
        users = User.objects.filter(username__icontains=querystring)    
        context = {"discussioni": discussioni, "posts": posts, "users": users}
        return render(request, "core/cerca.html", context)
    else:
        return render(request, "core/cerca.html")