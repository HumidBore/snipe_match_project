from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse

from .forms import DiscussioneModelForm, PostModelForm
from .mixins import StaffMixin
from .models import Discussione, Post, Sezione

# Create your views here.

class CreaSezione(StaffMixin, CreateView):  #eredita dalla classe generica per la creazione
    model = Sezione
    fields = "__all__" #specifico i campi del modello che mi servono
    template_name = "forum/crea_sezione.html"
    success_url = "/"   #url a cui andare (homepage) dopo aver creato

#visualizzo la sezione associata alla chiave specificata
def visualizza_sezione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    discussioni_sezione = Discussione.objects.filter(
        sezione_appartenenza=sezione
    ).order_by("-data_creazione")   #così ordino in modo che le più vecchie siano in fondo
    context = {"sezione": sezione, "discussioni": discussioni_sezione}
    return render(request, "forum/singola_sezione.html", context)

@login_required #decorator eche mi impone di essere loggato
def crea_discussione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    if request.method == "POST":
        form = DiscussioneModelForm(request.POST)
        if form.is_valid():
            #usando model form posso creare un oggetto discussione dalle cose passate nel form
            discussione = form.save(commit=False)   #con commit=False sospendo la creazione per un po', andando ad aggiungere altri attributi (ad esempio la sezione di appartenenza)
            discussione.sezione_appartenenza = sezione
            discussione.autore_discussione = request.user
            discussione.save()  #ora creo effettivamente l'oggetto(faccio il commit)
            primo_post = Post.objects.create(
                    discussione=discussione, 
                    autore_post=request.user,
                    contenuto=form.cleaned_data["contenuto"])   #uso il contenuto passato tramite form
            return HttpResponseRedirect(discussione.get_absolute_url())
    
    else:
        form = DiscussioneModelForm()

    context = {"form": form, "sezione": sezione}    #passo anche sezione nel context così nell'html dico la sezione in cui creo la nuova discussione
    return render(request, "forum/crea_discussione.html", context)

def visualizza_discussione(request, pk):
    discussione = get_object_or_404(Discussione, pk=pk)
    posts_discussione = Post.objects.filter(discussione=discussione) #mi prendo tutti i post di quella discussione
    
    paginator = Paginator(posts_discussione, 5) #voglio far vedere 5 post a pagina
    page = request.GET.get("pagina")
    posts = paginator.get_page(page)
    
    form_risposta = PostModelForm()
    context = {"discussione": discussione, 
        "posts_discussione": posts, #passo posts che è quello paginato
        "form_risposta": form_risposta} #ci metto anche il form di risposta
    return render(request, "forum/singola_discussione.html", context)

@login_required #decorator eche mi impone di essere loggato
def aggiungi_risposta(request, pk):     #pk della discssione a cui aggiungo il post
    discussione = get_object_or_404(Discussione, pk=pk)

    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.discussione = discussione
            form.instance.autore_post = request.user
            form.save()

            url_discussione = reverse("visualizza_discussione", kwargs={"pk": pk})  #prendo l'url che mi porta a visualizzare la discussione specificata
            pagine_in_discussione = discussione.get_n_pages()
            if pagine_in_discussione > 1:   #se ho più di una pagina reindirizzo all'ultima
                success_url = url_discussione + "?pagina=" + str(pagine_in_discussione)
                return HttpResponseRedirect(success_url)    
            else:   #se ho una sola pagina reindirizzo allla discussione
                return HttpResponseRedirect(url_discussione)    #rimando all'url della discussione dove ho aggiunto la risposta

    else:   #non mi interssano altri tipi di richieste, perchè se aggiungo una risposta devo inserire qualcosa!
        return HttpResponseBadRequest()
        
class CancellaPost(DeleteView):
    model = Post
    success_url = "/"

    #sovrascrivo il metodo per far si che possa eliminare solo i post che ha fatto l'utente loggato
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(autore_post_id=self.request.user.id)





