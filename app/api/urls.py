from django.urls import path

from api import views

urlpatterns = [
    path("survivors/", views.CreateSurvivorView.as_view()),
    path("survivors/<int:pk>/", views.RetrieveSurvivorView.as_view()),
    path("survivors/<int:pk>/location", views.UpdateSurvivorLocationView.as_view()),
    path("survivors/<int:pk>/infected", views.UpdateSurvivorInfectedView.as_view()),
    path("exchange/", views.ExchangeView.as_view()),
]
