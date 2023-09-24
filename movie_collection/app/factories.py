# factories.py
import factory
from app.models import User, Collection, Movie, Genre

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Sequence(lambda n: f'Genre {n}')

class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Sequence(lambda n: f'Movie {n}')
    description = 'Movie description'
    uuid = factory.Sequence(lambda n: f'uuid{n}')
    genres = factory.SubFactory(GenreFactory)

class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    title = factory.Sequence(lambda n: f'Collection {n}')
    description = 'Collection description'
    user = factory.SubFactory(UserFactory)
    movies = factory.SubFactory(MovieFactory)
