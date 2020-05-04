from rest_framework import serializers, generics
from api.model.comissao import Comissao


class ComissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comissao
        fields = (
            'cargo', 'id_parlamentar', 'partido', 'uf', 'situacao',
            'nome', 'foto', 'sigla', 'casa')


class ComissaoList(generics.ListAPIView):
    '''
    A partir da casa (camara ou senado) e da sigla da Comissão lista os parlamentares
    que fazem parte da Comissão com informações como cargo e situação.
    '''
    serializer_class = ComissaoSerializer

    def get_queryset(self):
        '''
        Retorna a comissao filtrada
        '''
        casa_parametro = self.kwargs['casa']
        sigla_parametro = self.kwargs['sigla']
        return Comissao.objects.filter(
            casa=casa_parametro, sigla=str.upper(sigla_parametro))
