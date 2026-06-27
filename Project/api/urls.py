from django.urls import path
from . import views

urlpatterns = [
    path('singobj/<int:id>/',views.singobj),
    path('multiobj/',views.multiobj),
]
