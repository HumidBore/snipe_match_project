from django.shortcuts import render

from django.views.generic.list import ListView

from .utils import EventsGetter

from .forms import ThreeOutcomesFiltersForm
from django.contrib.auth.decorators import login_required
from .forms import TwoOutcomesFiltersForm

from .models import ScrapingResults

# Create your views here.

@login_required
def two_outcomes_matches(request):
    events = EventsGetter.get_matches(2, #stands for two outcomes table
                                    RTPFrom=request.POST.get('RTPFrom'),
                                    RTPTo=request.POST.get('RTPTo'),
                                    dateFrom=request.POST.get('dateFrom'),
                                    dateTo=request.POST.get('dateTo'),
                                    bookmaker1=request.POST.getlist('bookmaker1'),
                                    betOdd1From=request.POST.get('betOdd1From'),
                                    betOdd1To=request.POST.get('betOdd1To'),
                                    bet1=request.POST.get('bet1'),
                                    bookmaker2=request.POST.getlist('bookmaker2'),
                                    betOdd2From=request.POST.get('betOdd2From'),
                                    betOdd2To=request.POST.get('betOdd2To'),
                                    bet2=request.POST.get('bet2')
                                    )
    if request.method == "POST":
        form = TwoOutcomesFiltersForm(request.POST)
    else:
        form = TwoOutcomesFiltersForm()
    context = {"form": form, "events": events}
    return render(request, "betmatcher/due_esiti.html", context)

@login_required
def three_outcomes_matches(request):
    events = EventsGetter.get_matches(3, #stands for three outcomes table
                                    RTPFrom=request.POST.get('RTPFrom'),
                                    RTPTo=request.POST.get('RTPTo'),
                                    dateFrom=request.POST.get('dateFrom'),
                                    dateTo=request.POST.get('dateTo'),
                                    bookmaker1=request.POST.getlist('bookmaker1'),
                                    betOdd1From=request.POST.get('betOdd1From'),
                                    betOdd1To=request.POST.get('betOdd1To'),
                                    bet1=request.POST.getlist('bet1'),
                                    bookmaker2=request.POST.getlist('bookmaker2'),
                                    betOdd2From=request.POST.get('betOdd2From'),
                                    betOdd2To=request.POST.get('betOdd2To'),
                                    bet2=request.POST.getlist('bet2'),
                                    bookmaker3=request.POST.getlist('bookmaker3'),
                                    betOdd3From=request.POST.get('betOdd3From'),
                                    betOdd3To=request.POST.get('betOdd3To'),
                                    bet3=request.POST.getlist('bet3')
                                    )
    if request.method == "POST":
        form = ThreeOutcomesFiltersForm(request.POST)
    else:
        form = ThreeOutcomesFiltersForm()
    # context = {"form": form, "available_books": available_books, "available_bets": available_bets, "events": events}
    context = {"form": form, "events": events}
    return render(request, "betmatcher/tre_esiti.html", context)