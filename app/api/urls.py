from django.urls import path
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api import views

schema_view = get_schema_view(
    openapi.Info(
        title="Teste Infog2",
        description="Teste de codificação de desenvolvedor",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("survivors/", views.CreateSurvivorView.as_view()),
    path("survivors/<int:pk>/", views.RetrieveSurvivorView.as_view()),
    path("survivors/<int:pk>/location/", views.UpdateSurvivorLocationView.as_view()),
    path("survivors/<int:pk>/infected/", views.UpdateSurvivorInfectedView.as_view()),
    path("exchange/", views.ExchangeView.as_view()),
    path("reports/", views.ReportsView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path("docs/", schema_view.with_ui("swagger", cache_timeout=0)),
    ]
