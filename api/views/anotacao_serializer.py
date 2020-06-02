from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.model.anotacao import Anotacao
from datetime import datetime


class AnotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anotacao
        fields = (
            "id_leggo",
            "interesse",
            "data_criacao",
            "data_ultima_modificacao",
            "autor",
            "categoria",
            "titulo",
            "anotacao",
            "peso",
        )


class AnotacaoListByProp(generics.ListAPIView):
    """
    Apresenta uma lista com as anotações feitas sobre as proposições por
    interesses abordados pelo Leggo. As anotações são compostas por data de
    criação e última modificação, autor, titulo, conteúdo, peso de importância e
    interesse relacionado.
    """

    serializer_class = AnotacaoSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "Id da proposição no sistema do Leg.go",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "interesse",
                openapi.IN_PATH,
                "Nome do interesse-alvo",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "peso",
                openapi.IN_PATH,
                "Peso máximo das anotações",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "ultimas_n",
                openapi.IN_PATH,
                "Número máximo de retorno das últimas anotações",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def get_queryset(self):
        """
        Retorna anotações associadas a uma PL feitas por um interesse
        """

        interesseArg = self.request.query_params.get("interesse")
        peso = self.request.query_params.get("peso", 100)
        ultimos_n = self.request.query_params.get("ultimas_n", 10)
        id_leggo = self.kwargs["id"]

        if not interesseArg:
            interesseArg = "leggo"

        queryset = Anotacao.objects.filter(id_leggo=id_leggo, interesse=interesseArg)

        if peso:
            queryset = queryset.order_by("peso", "-data_ultima_modificacao").filter(
                peso__lte=peso
            )

        if ultimos_n:
            queryset = queryset[: int(ultimos_n)]

        return queryset


class AnotacaoList(generics.ListAPIView):
    """
    Apresenta uma lista com as últimas anotações feitas sobre todas proposições por
    interesses abordados pelo Leggo. As anotações são compostas por data de
    criação e última modificação, autor, titulo, conteúdo, peso de importância e
    interesse relacionado.
    """

    serializer_class = AnotacaoSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "interesse",
                openapi.IN_PATH,
                "Nome do interesse-alvo",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "data_inicio",
                openapi.IN_PATH,
                "data de início do período de tempo ao qual " +
                "as anotações devem ser modificadas",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "data_fim",
                openapi.IN_PATH,
                "data de fim do período de tempo ao qual " +
                "as anotações devem ser modificadas",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "peso",
                openapi.IN_PATH,
                "Peso máximo",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "ultimas_n",
                openapi.IN_PATH,
                "Número máximo de retorno das últimas anotações",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def get_queryset(self):
        """
        Retorna as últimas anotações de todas as proposições de um interesse
        """

        interesseArg = self.request.query_params.get("interesse")
        data_inicio = self.request.query_params.get("data_inicio", None)
        data_fim = self.request.query_params.get("data_fim", None)
        peso = self.request.query_params.get("peso", 100)
        ultimos_n = self.request.query_params.get("ultimas_n", 10)

        data_inicio_dt = None
        data_fim_dt = None

        if not interesseArg:
            interesseArg = "leggo"

        queryset = Anotacao.objects.filter(interesse=interesseArg)

        try:
            if data_inicio is not None:
                data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        except ValueError:
            print(f"Data de início ({data_inicio}) inválida. ")
            data_inicio_dt = None

        try:
            data_fim_dt = (
                datetime.today()
                if data_fim is None
                else datetime.strptime(data_fim, "%Y-%m-%d")
            )
        except ValueError:
            print(
                f"Data de fim ({data_fim}) inválida. "
                "Utilizando data atual como data de fim."
            )
            data_fim_dt = datetime.today()

        if data_inicio_dt is not None:
            queryset = queryset.filter(data_ultima_modificacao__gte=data_inicio_dt)

        queryset = queryset.filter(data_ultima_modificacao__lte=data_fim_dt)

        if peso:
            queryset = queryset.order_by("peso", "-data_ultima_modificacao").filter(
                peso__lte=peso
            )

        if ultimos_n:
            queryset = queryset[: int(ultimos_n)]

        return queryset
