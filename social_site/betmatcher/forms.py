from django import forms
from crispy_forms.helper import FormHelper
from .utils import EventsGetter


class ThreeOutcomesFiltersForm(forms.Form):  #max_digits=5, decimal_places=2, label='RTP:', 
    #, label='', widget=PrependWidget(base_widget=forms.NumberInput, data='da')
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)

    books1 = EventsGetter.get_available_bookmakers()
    books2 = EventsGetter.get_available_bookmakers()
    books3 = EventsGetter.get_available_bookmakers()

    RTPFrom = forms.DecimalField(label='', required=False)
    RTPTo = forms.DecimalField(label='', required=False)
    dateFrom = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], label='', required=False)
    dateTo = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], label='', required=False)
    
    bookmaker1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EventsGetter.get_available_bookmakers(), label='', required=False)
    betOdd1From = forms.DecimalField(widget=forms.NumberInput, label='', required=False)
    betOdd1To = forms.DecimalField(label='', required=False)
    bet1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EventsGetter.get_available_bets(3), label='', required=False)
    
    bookmaker2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EventsGetter.get_available_bookmakers(), label='', required=False)
    betOdd2From = forms.DecimalField(label='', required=False)
    betOdd2To = forms.DecimalField(label='', required=False)
    bet2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EventsGetter.get_available_bets(3), label='', required=False)
    
    bookmaker3 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EventsGetter.get_available_bookmakers(), label='', required=False)
    betOdd3From = forms.DecimalField(label='', required=False)
    betOdd3To = forms.DecimalField(label='', required=False)
    bet3 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EventsGetter.get_available_bets(3), label='', required=False)

class TwoOutcomesFiltersForm(forms.Form):  #max_digits=5, decimal_places=2, label='RTP:', 
    #, label='', widget=PrependWidget(base_widget=forms.NumberInput, data='da')
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)

    books1 = EventsGetter.get_available_bookmakers()
    books2 = EventsGetter.get_available_bookmakers()

    RTPFrom = forms.DecimalField(label='', required=False)
    RTPTo = forms.DecimalField(label='', required=False)
    dateFrom = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], label='', required=False)
    dateTo = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], label='', required=False)
    
    bookmaker1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EventsGetter.get_available_bookmakers(), label='', required=False)
    betOdd1From = forms.DecimalField(widget=forms.NumberInput, label='', required=False)
    betOdd1To = forms.DecimalField(label='', required=False)
    bet1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EventsGetter.get_available_bets(2), label='', required=False)
    
    bookmaker2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EventsGetter.get_available_bookmakers(), label='', required=False)
    betOdd2From = forms.DecimalField(label='', required=False)
    betOdd2To = forms.DecimalField(label='', required=False)
    bet2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EventsGetter.get_available_bets(2), label='', required=False)
    