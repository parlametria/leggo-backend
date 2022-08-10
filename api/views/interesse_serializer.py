from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.model.interesse import Interesse


class InteresseProposicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interesse
        fields = (
            "interesse",
            "temas",
            "slug_temas",
            "apelido",
            "advocacy_link",
            "tipo_agenda"
        )


class InteresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interesse
        fields = (
            "interesse",
            "nome_interesse",
            "temas",
            "slug_temas",
            "apelido",
            "advocacy_link",
            "tipo_agenda"
        )


class InteresseList(generics.ListAPIView):
    """
    Apresenta lista com mapeamento entre as proposições analisadas e os
    interesses abordados pelo Leggo. Um interesse é um assunto geral
    no qual um conjunto de proposições está relacionado. O primeiro
    interesse analisado pelo Leggo é o da RAC, que é uma rede de
    organizações que atua no Congresso em diferentes eixos como
    Meio Ambiente, Direitos Humanos, Nova Economia e Transparência.
    Outros possíveis interesses seriam Primeira Infância (conjunto
    de proposições ligadas a direitos e deveres relacionados às
    crianças).
    """

    serializer_class = InteresseSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                "id da proposição no sistema do Leg.go",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def get_queryset(self):
        """
        Retorna interesses associados a uma PL
        """
        id_prop = self.kwargs["id"]
        return Interesse.objects.filter(id_leggo=id_prop)


class TemaSerializer(serializers.Serializer):
    tema = serializers.CharField()
    tema_slug = serializers.CharField()


class TemaList(generics.ListAPIView):
    """
    Retorna lista de temas associados a uma agenda.
    """

    serializer_class = TemaSerializer

    def get_queryset(self):

        interesse_arg = self.request.query_params.get("interesse")
        if interesse_arg is None:
            interesse_arg = "leggo"

        queryset = (
            Interesse.objects.all().filter(interesse=interesse_arg)
            .distinct("tema")
        )

        temas = []
        for tema_list in queryset:
            if len(tema_list.obj_temas) and tema_list.obj_temas[0]['tema'] != 'nan':
                temas.extend(tema_list.obj_temas)

        lista_temas = list({v["tema_slug"]: v for v in temas}.values())
        lista_temas.sort(key=lambda item: item["tema_slug"])

        return lista_temas


class InteresseByNomeSerializer(serializers.Serializer):
    interesse = serializers.CharField()
    nome_interesse = serializers.CharField()
    descricao_interesse = serializers.CharField()


class InteresseByNome(generics.ListAPIView):
    """
    Retorna nome de agenda com base no interesse recebido.
    """

    serializer_class = InteresseByNomeSerializer

    def get_queryset(self):

        interesse_arg = self.request.query_params.get("interesse")

        queryset = (
            Interesse.objects.all()
            .distinct("interesse", "nome_interesse", "descricao_interesse")
        )

        if interesse_arg:
            queryset = queryset.filter(interesse=interesse_arg)
        return queryset
