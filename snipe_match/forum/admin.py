from django.contrib import admin
from .models import Discussione, Post, Sezione
# Register your models here.

class DiscussioneModelAdmin(admin.ModelAdmin): #le uso per personalizzare la sezione admin 
    model = Discussione
    list_display = ["titolo", "sezione_appartenenza", "autore_discussione"] #campi da mostrare
    search_fields = ["titolo", "autore_discussione"]    #campi ricercabili
    list_filter = ["sezione_appartenenza", "data_creazione"]   #campi filtrabili 

class PostModelAdmin(admin.ModelAdmin): #le uso per personalizzare la sezione admin 
    model = Post
    list_display = ["autore_post", "discussione"] #campi da mostrare
    search_fields = ["contenuto"]    #campi ricercabili
    list_filter = ["data_creazione", "autore_post", ]   #campi filtrabili 

class SezioneModelAdmin(admin.ModelAdmin): #le uso per personalizzare la sezione admin 
    model = Sezione
    list_display = ["nome_sezione", "descrizione"] #campi da mostrare
    
admin.site.register(Discussione, DiscussioneModelAdmin) #gli passo anche il modello di admin
admin.site.register(Post, PostModelAdmin)
admin.site.register(Sezione, SezioneModelAdmin)

