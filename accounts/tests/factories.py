import factory
from django.contrib.auth.hashers import make_password
from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    name = factory.Faker('name')
    password = factory.LazyFunction(lambda: make_password('testpassword123'))

    class Meta:
        model = User
