from drf_yasg import openapi

from api import serializers

survivor_create = dict(
    tags=["Sobreviventes"],
    request_body=serializers.CreateSurvivorSerializer,
    operation_description="Registrar um novo sobrevivente no sistema",
    operation_id="criar_sobrevivente",
    responses={
        201: openapi.Response(
            description="Sobrevivente registrado",
            schema=serializers.SurvivorSerializer,
        ),
    },
)

survivor_retrieve = dict(
    tags=["Sobreviventes"],
    operation_description="Consultar um sobrevivente no sistema",
    operation_id="consultar_sobrevivente",
    responses={
        200: openapi.Response(
            description="Sobrevivente consultado",
            schema=serializers.SurvivorSerializer,
        ),
    },
)

update_survivor_location = dict(
    tags=["Sobreviventes"],
    operation_description="Atualizar a localização de um sobrevivente",
    operation_id="atualizar_localizacao",
    request_body=serializers.UpdateSurvivorLocationSerializer,
    responses={
        200: openapi.Response(
            description="Localização atualizada",
            schema=serializers.SurvivorSerializer,
        ),
    },
)

update_survivor_infected = dict(
    tags=["Sobreviventes"],
    operation_description="Reportar sobrevivente infectado",
    operation_id="reportar_sobrevivente_infectado",
    responses={
        200: openapi.Response(
            description="Sobrevivente infectado atualizado",
            schema=serializers.SurvivorSerializer,
        ),
    },
)

exchange_items = dict(
    tags=["Trocas"],
    operation_description="Realizar troca de itens entre sobreviventes",
    operation_id="realizar_troca",
    request_body=serializers.ExchangeSerializer,
    responses={
        204: openapi.Response(
            description="Trocas realizadas com sucesso",
        )
    },
)

reports = dict(
    tags=["Relatórios"],
    operation_description="Consultar relatórios sobre os sobreviventes",
    operation_id="consultar_relatorios",
    responses={
        200: openapi.Response(
            description="Resultados",
            schema=serializers.ReportsSerializer,
        ),
    },
)
