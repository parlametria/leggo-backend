from os import getenv
from requests import post as post_request

from django.contrib.auth.models import User
from django.core.validators import validate_email

from rest_framework import serializers, generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request

from usuario.models import Perfil, VerfificacaoEmail


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


class VerfificacaoEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerfificacaoEmail
        fields = "__all__"


class UsuarioList(generics.CreateAPIView):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()

    def perform_create(self, serializer: PerfilSerializer):
        data = serializer.data.copy()
        usuario_data = data["usuario"]
        # password is write_only, so it is not present on serializer.data
        usuario_data["password"] = serializer.get_initial()["usuario"]["password"]

        self._verify_email(usuario_data["email"])

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

        verfificacao_email = VerfificacaoEmail(usuario=usuario)
        verfificacao_email.save()
        enviar_email_verificacao(verfificacao_email)

        return instance

    def _verify_email(self, email: str):
        try:
            validate_email(email)
        except Exception:
            raise ValidationError(detail={"email": "Valor inválido"})

        found = User.objects.filter(email=email)
        if len(found) > 0:
            raise ValidationError(detail={"email": "Já está em uso"})


class UsuarioDetail(generics.RetrieveAPIView):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()
    permission_classes = (IsOwnerOrAdminPermission,)


class VerificaEmailDetail(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = VerfificacaoEmailSerializer
    queryset = VerfificacaoEmail.objects.all()
    lookup_field = "token"

    def update(self, request: Request, *args, **kwargs):
        instance: VerfificacaoEmail = self.get_object()

        instance.verificado = True
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


def _enviar_email(to_email: str, subject: str, html: str):
    MAILGUN_FROM_EMAIL = getenv("MAILGUN_FROM_EMAIL")
    MAILGUN_API_URL = getenv("MAILGUN_API_URL")
    MAILGUN_API_KEY = getenv("MAILGUN_API_KEY")

    data = {
        "from": MAILGUN_FROM_EMAIL,
        "to": to_email,
        "subject": subject,
        "html": html,
    }

    response = post_request(
        MAILGUN_API_URL,
        auth=("api", MAILGUN_API_KEY),
        data=data,
    )

    return response


def enviar_email_verificacao(verfificacao_email: VerfificacaoEmail):
    MAILGUN_PARLAMETRIA_FRONTEND = getenv("MAILGUN_PARLAMETRIA_FRONTEND")

    email = verfificacao_email.usuario.email
    link_verificacao = "".join(
        [
            MAILGUN_PARLAMETRIA_FRONTEND,
            "/verificacao-email/",
            str(verfificacao_email.token),
        ]
    )

    html = """
        <html>
            <body>
                <h1>Verificação de e-mail do parlametria</h1>
                <p>
                    Este e-mail foi enviado automaticamente, caso não tenha
                    se cadastrado no parlametria, por favor apenas ignore esse mail.
                </p>
                <p>
                    Para finalizar a criação de sua conta,
                    por favor clique no link abaixo:
                    <a href='%s'>%s</a>
                </p>
            </body>
        </html>
        """ % (
        link_verificacao,
        link_verificacao,
    )

    response = _enviar_email(email, "Verificação de e-mail parlametria", html)

    if response.status_code != 200:
        raise ValidationError(
            detail={"email": "Não foi possível enviar o email de confirmação."}
        )

    return response
