from django.urls import path

from .views import CreateSurvivorView

urlpatterns = [
    path("", CreateSurvivorView.as_view()),
]
