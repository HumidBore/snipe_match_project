from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User #poichè sono gli utenti ad interagire (es creare i post)
import math #i serve la ceil per sapere quante pagine ha una discussione partendo dal numero di post
# Create your models here.

class Sezione(models.Model):
    """ 
    le sezioni dividono il sito per categorie di discussione.
    Ciascuna sezione contiene svariate discussioni.
    Le sezioni sono create dagli admin del sito
    """

    nome_sezione = models.CharField(max_length=80)
    descrizione = models.CharField(max_length=150, blank=True, null=True)   #blank: può non essere presente il campo; null: ouò essere null
    logo_sezione = models.ImageField(blank=True, null=True)
    #non metto un campo utenet perchè sono gli admin a gestire le sezioni

    def __str__(self):
        return self.nome_sezione

    #così mi si crea dinamicamente il linnk alla sezione
    def get_absolute_url(self):
        return reverse("sezione_view", kwargs={"pk": self.pk})  #gli passo come argomento la chiave primaria, perchè serve per riscostruire l'url

    def get_last_discussions(self): #prendo le ultime due discussioni
        return Discussione.objects.filter(sezione_appartenenza=self).order_by("-data_creazione")[:2]    #sottolista con le ultime due discussioni

    def get_number_of_posts_in_section(self):
        #query che returna tutti i post che hanno che sono relativi ad una discussione nella sezione self
        return Post.objects.filter(discussione__sezione_appartenenza=self).count()

    class Meta:
        verbose_name = "Sezione"
        verbose_name_plural = "Sezioni"



class Discussione(models.Model):
    
    titolo = models.CharField(max_length=120)
    data_creazione = models.DateTimeField(auto_now_add=True)   #auto_now_add setta la adata quando è creata la discussione
    autore_discussione = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discussioni")  #col related accedo facilmente alle discussioni create da un utente
    sezione_appartenenza = models.ForeignKey(Sezione, on_delete=models.CASCADE)


    def __str__(self):
        return self.titolo

    def get_absolute_url(self):
        return reverse("visualizza_discussione", kwargs={"pk": self.pk})  #gli passo come argomento la chiave primaria, perchè serve per riscostruire l'url

    def get_n_pages(self):
        posts_discussione = self.post_set.count()
        n_pagine = math.ceil(posts_discussione / 5)  #divido per 5 perchè ho messo 5 posts per pagina
        return n_pagine

    class Meta:
        verbose_name = "Discussione"
        verbose_name_plural = "Discussioni"

class Post(models.Model):
    autore_post = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    contenuto = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)   #auto_now_add setta la adata quando è creata la discussione
    discussione = models.ForeignKey(Discussione, on_delete=models.CASCADE)

    def __str__(self):
        return self.autore_post.username

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
