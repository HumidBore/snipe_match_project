from django import forms

from .models import Discussione



class DiscussioneModelForm(forms.ModelForm):
    contenuto = forms.CharField(    #passo un widget textarea per avere più spazio per scrivere
        widget = forms.Textarea(attrs={"placeholder": "Di cosa vuoi parlarci?"}),
        max_length=4000, 
        label = "Primo Messaggio"
    )

    class Meta:
        model = Discussione
        fields = ["titolo", "contenuto"]    #campi del form
        widget = {#specifico i widget da usare per i campi
            "titolo": forms.TextInput(attrs={"placeholder": "Titolo della discussione"})
        }




