from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="homepage"),
    path("users/", views.UserList.as_view(), name="user_list"), #uso as_view() perchè è una view class based (non è un metodo come le altre, è una classe che estende ListView)
    path("user/<str:username>/", views.user_profile_view, name="user_profile"),
    path("cerca/", views.cerca, name="funzione_cerca"), 
]