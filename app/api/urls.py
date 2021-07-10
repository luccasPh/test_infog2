from django.urls import path

from api import views

urlpatterns = [
    path("", views.CreateSurvivorView.as_view()),
    path("<int:pk>/location", views.UpdateSurvivorLocationView.as_view()),
    path("<int:pk>/infected", views.UpdateSurvivorInfectedView.as_view()),
]
