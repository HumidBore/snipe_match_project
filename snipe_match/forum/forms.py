from django import forms

from .models import Discussione, Post


class DiscussioneModelForm(forms.ModelForm):
    contenuto = forms.CharField(    #passo un widget textarea per avere più spazio per scrivere
        widget = forms.Textarea(attrs={"placeholder": "Di cosa vuoi parlarci?"}),
        max_length=4000, 
        label = "Primo Messaggio"
    )

    class Meta:
        model = Discussione
        fields = ["titolo", "contenuto"]    #campi del form
        widgets = {#specifico i widget da usare per i campi
            "titolo": forms.TextInput(attrs={"placeholder": "Titolo della discussione"})
        }


class PostModelForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["contenuto"] 
        widgets = {
            "contenuto": forms.Textarea(attrs={'rows': '5'})  #voglio una textarea di 5 righe, sennò sembra troppoo grossa
        }
        labels = {
            "contenuto": "Messaggio"
        }
