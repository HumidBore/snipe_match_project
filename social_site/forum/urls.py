from django.urls import path
from . import views

urlpatterns = [
    path('nuova-sezione/', views.CreaSezione.as_view(), name="crea_sezione"),    #as_view perchè è una class based view
    path('sezione/<int:pk>', views.visualizza_sezione, name="sezione_view"),    
    path('sezione/<int:pk>/crea-discussione', views.crea_discussione, name="crea_discussione"),
    path('discussione/<int:pk>', views.visualizza_discussione, name="visualizza_discussione_view"),    
]



