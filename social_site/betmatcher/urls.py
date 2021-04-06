from django.urls import path
from . import views

urlpatterns = [
    path("due-esiti/", views.two_outcomes_matches, name="two_outcomes_list"),
    path("tre-esiti/", views.three_outcomes_matches, name="three_outcomes_list"),

]