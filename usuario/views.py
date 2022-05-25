from rest_framework import serializers, generics, permissions
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from usuario.models import Profile


class IsOwnerOrAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view, **kwargs):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.user.is_staff


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
            "password": {"write_only": True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False)

    class Meta:
        model = Profile
        fields = (
            "empresa",
            "usuario",
        )


class UsuarioList(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def perform_create(self, serializer: ProfileSerializer):
        data = serializer.data.copy()
        usuario_data = data["usuario"]
        # password is write_only so it is not present on data
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

        instance: Profile = Profile(empresa=data["empresa"], usuario=usuario)
        instance.save()

        return instance


class UsuarioDetail(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsOwnerOrAdminPermission,)
