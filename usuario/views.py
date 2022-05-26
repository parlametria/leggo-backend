from rest_framework import serializers, generics, permissions
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from usuario.models import Perfil


class IsOwnerOrAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view, **kwargs):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj: Perfil):
        return obj.usuario.id == request.user.id or request.user.is_staff


class UsuarioSerializer(serializers.ModelSerializer):
    email = serializers.CharField(allow_blank=False)
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
        )
        read_only_fields = ("is_active", "is_staff")
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }


class PerfilSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False)

    class Meta:
        model = Perfil
        fields = (
            "empresa",
            "usuario",
        )


class UsuarioList(generics.CreateAPIView):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()

    def perform_create(self, serializer: PerfilSerializer):
        data = serializer.data.copy()
        usuario_data = data["usuario"]
        # password is write_only, so it is not present on serializer.data
        usuario_data["password"] = serializer.get_initial()["usuario"]["password"]

        found = User.objects.filter(email=usuario_data["email"])
        if len(found) > 0:
            raise ValidationError(detail={"email": "Já está em uso"})

        usuario = User(
            username=usuario_data["email"],
            email=usuario_data["email"],
            first_name=usuario_data["first_name"],
            last_name=usuario_data["last_name"],
        )
        usuario.set_password(usuario_data["password"])
        usuario.save()

        instance = Perfil(empresa=data["empresa"], usuario=usuario)
        instance.save()

        return instance


class UsuarioDetail(generics.RetrieveAPIView):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()
    permission_classes = (IsOwnerOrAdminPermission,)
