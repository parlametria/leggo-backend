from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import Perfil
from .views import UsuarioList, UsuarioDetail


class PerfilModelTests(TestCase):
    def setUp(self):
        user1 = User.objects.create(
            username="perfiluser1@email.com",
            password="perfiluser1@email.com",
            email="perfiluser1@email.com",
            first_name="Perfil",
            last_name="User",
        )
        self.perfil = Perfil.objects.create(usuario=user1, empresa="Testing")

    def test_Perfil_is_a_user(self):
        """Perfil is a user, so its id is the user id"""
        _id = getattr(self.perfil, "id", None)
        self.assertTrue(_id is None)

        _id = self.perfil.usuario.id
        self.assertTrue(Perfil.objects.get(pk=_id) is not None)


class UsuarioListViewTests(TestCase):
    BASE_URL = "/usuarios/"

    def setUp(self):
        user1 = User.objects.create(
            username="Perfiluser1@email.com",
            email="Perfiluser1@email.com",
            first_name="Perfil",
            last_name="user",
            password="Perfiluser1@email.com",
        )
        self.perfil = Perfil.objects.create(usuario=user1, empresa="Testing")
        self.api = APIRequestFactory()

    def test_create_a_new_user(self):
        """Should create a mew user"""
        post_data = {
            "empresa": "It Works",
            "usuario": {
                "email": "newuser@email.com",
                "password": "newuser@email.com",
                "first_name": "newuser@email.com",
                "last_name": "newuser@email.com",
            },
        }
        old_user_count = User.objects.count()
        old_Perfil_count = Perfil.objects.count()

        request = self.api.post(self.BASE_URL, data=post_data, format="json")
        view = UsuarioList.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, post_data)
        self.assertEqual(User.objects.count(), old_user_count + 1)
        self.assertEqual(Perfil.objects.count(), old_Perfil_count + 1)

    def test_set_username_as_the_same_value_as_email(self):
        """A user's username must be set as the same value as the email"""
        post_data = {
            "empresa": "",
            "usuario": {
                "email": "newuser@email.com",
                "password": "newuser@email.com",
                "first_name": "new",
                "last_name": "user",
            },
        }

        request = self.api.post(self.BASE_URL, data=post_data, format="json")
        view = UsuarioList.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["usuario"]["email"], post_data["usuario"]["email"]
        )

        user = User.objects.filter(username=post_data["usuario"]["email"]).first()
        self.assertNotEqual(user, None)
        self.assertEqual(user.email, post_data["usuario"]["email"])
        self.assertEqual(user.username, post_data["usuario"]["email"])

    def test_first_and_last_names_cant_be_empty(self):
        """Both first_name and last_name cant be empty"""
        post_data = {
            "empresa": "",
            "usuario": {
                "email": "newuser@email.com",
                "password": "newuser@email.com",
                "first_name": "",
                "last_name": "",
            },
        }
        old_user_count = User.objects.count()
        old_Perfil_count = Perfil.objects.count()

        request = self.api.post(self.BASE_URL, data=post_data, format="json")
        view = UsuarioList.as_view()
        response = view(request)
        errors = response.data["usuario"]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(errors["first_name"][0], "This field may not be blank.")
        self.assertEqual(errors["last_name"][0], "This field may not be blank.")
        self.assertEqual(User.objects.count(), old_user_count)
        self.assertEqual(Perfil.objects.count(), old_Perfil_count)


class UsuarioDetailViewTests(TestCase):
    BASE_URL = "/usuarios"

    def setUp(self):
        self.api = APIRequestFactory()
        for n in range(3):
            user = User.objects.create(
                username="Perfiluser%d@email.com" % n,
                email="Perfiluser%d@email.com" % n,
                first_name="Perfil %d" % n,
                last_name="user %d" % n,
                password="Perfiluser%d@email.com" % n,
                is_staff=n == 0,
            )
            Perfil.objects.create(usuario=user, empresa="Testing %d" % n)

    def test_non_authenticated_user_cant_see_users_details(self):
        """A non authenticated user can't see users details"""

        request = self.api.get(f"{self.BASE_URL}/1", format="json")
        view = UsuarioDetail.as_view()
        response = view(request, pk=1)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_non_staff_can_see_his_details(self):
        """A non staff user can see his details"""

        user = User.objects.filter(is_staff=False)[0]
        self.assertEqual(user.is_staff, False)

        request = self.api.get(f"{self.BASE_URL}/{user.id}", format="json")
        force_authenticate(request, user=user)
        view = UsuarioDetail.as_view()
        response = view(request, pk=user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["empresa"], user.perfil.empresa)
        self.assertEqual(response.data["usuario"]["id"], user.id)
        self.assertEqual(response.data["usuario"]["email"], user.username)
        self.assertEqual(response.data["usuario"]["email"], user.email)

    def test_non_staff_cant_see_other_user_details(self):
        """A non staff user can't see other user details"""

        [non_staff_user1, non_staff_user2, *_] = User.objects.filter(is_staff=False)

        self.assertEqual(non_staff_user1.is_staff, False)
        self.assertEqual(non_staff_user2.is_staff, False)

        request = self.api.get(f"{self.BASE_URL}/{non_staff_user1.id}", format="json")
        # authenticate as non_staff_user2 and try to see the details of non_staff_user1
        force_authenticate(request, user=non_staff_user2)
        view = UsuarioDetail.as_view()
        response = view(request, pk=non_staff_user1.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_a_staff_user_can_see_other_user_details(self):
        """A staff can see other user details"""

        staff_user = User.objects.filter(is_staff=True).first()
        non_staff_user = User.objects.filter(is_staff=False).first()

        self.assertEqual(staff_user.is_staff, True)
        self.assertEqual(non_staff_user.is_staff, False)

        request = self.api.get(f"{self.BASE_URL}/{non_staff_user.id}", format="json")
        # authenticate as staff_user and try to see the details of non_staff_user
        force_authenticate(request, user=staff_user)
        view = UsuarioDetail.as_view()
        response = view(request, pk=non_staff_user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["empresa"], non_staff_user.perfil.empresa)
        self.assertEqual(response.data["usuario"]["id"], non_staff_user.id)
        self.assertEqual(response.data["usuario"]["email"], non_staff_user.username)
        self.assertEqual(response.data["usuario"]["email"], non_staff_user.email)
