from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User #devo importaare il modello che riempo col form
from accounts.forms import FormRegistrazione #form di registrazione definito



# Create your views here.

def registrazione_view(request):
    if request.method == "POST":    #se ricevo una richiesta post, cioè mi mandano dati
        form = FormRegistrazione(request.POST)  #inizializzo il form con i dati che mi hanno passato
        if form.is_valid(): #se valido prendo i dati che mi interessano
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]   #prendo la 1, la 2 era per confermare fossero uguali
            User.objects.create_user(username=username, #creo uno user dai dati passati
                                    password=password,
                                    email=email
                                    )
            user = authenticate(username=username,    #autentico lo user
                            password=password)
            login(request, user)    #faccio il login vero e proprio

            return HttpResponseRedirect("/")    #riporto l'utente nella homepage
    else:   #se la richiesta non è post
        form = FormRegistrazione()  #inizializzo lo stesso il form
    #qui ci vado quando il form è richiesto per la prima volta in pratica
    context = {"form": form}
    return render(request, "accounts/registrazione.html", context)   #gli passo il template da renderizzare

