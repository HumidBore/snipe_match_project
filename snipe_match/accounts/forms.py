from django import forms
from django.contrib.auth.forms import UserCreationForm  #usato per registarre un nuovo utente
from django.contrib.auth.models import User #modello base di django per un utente


class FormRegistrazione(UserCreationForm):
    #oltre ai campi della classe madre, ho bisogno anche della mail
    email = forms.CharField(max_length=30, required=True, widget=forms.EmailInput()) #

    class Meta:
        model = User    #uso modello base django
        fields = ["username", "email", "password1", "password2"]  #campi del form che uso











