import datetime

import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: 'username_{}'.format(n))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

    is_active = True
    is_staff = False
    is_superuser = False

    last_login = factory.LazyAttribute(lambda _o: datetime.datetime(2000, 1, 1, tzinfo=None))
    date_joined = factory.LazyAttribute(lambda _o: datetime.datetime(1999, 1, 1, tzinfo=None))
