from rest_framework import serializers
from .models import User, Collection, Movie, Genre
import re


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


    def validate_username(self, value):
       
        # Check if username contains only letters (no digits or special characters)
        if not re.match("^[a-zA-Z]+$", value):
            raise serializers.ValidationError("Username should only contain letters.")
        
        return value

    def validate_password(self, value):
        
        if len(value) < 8:
            raise serializers.ValidationError("Password should be at least 8 characters long.")
        
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("Password should contain at least one special character.")
        
        return value

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class MovieSerializer(serializers.ModelSerializer):
    # genres = GenreSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = ['title', 'description', 'uuid', 'genres']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        genre_names = [genre['name'] for genre in data['genres']]
        data['genres'] = ', '.join(genre_names)
        return data
    

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)  

    class Meta:
        model = Collection
        fields = ['title', 'description', 'collection_ting', 'movies']


class MovieSerializer2(serializers.ModelSerializer):
    genres = serializers.ListField(child=serializers.CharField(max_length=255))

    class Meta:
        model = Movie
        fields = ['title', 'description', 'uuid', 'genres']


class CreateCollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer2(many=True)  


    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']

    
    def validate_title(self, value):
        # Check if a collection with the same title and user already exists
        user = self.context['request'].user
        existing_collection = Collection.objects.filter(title=value, user=user).first()
        if existing_collection:
            raise serializers.ValidationError("A collection with this title already exists for this user.")
        
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        
        return value
    
    def validate_movies(self, value):
        movie_uuids = [movie_data['uuid'] for movie_data in value]

        # Check for duplicate UUIDs within the same collection
        if len(movie_uuids) != len(set(movie_uuids)):
            raise serializers.ValidationError("A movie cannot be added more than once to the same collection.")

        return value


    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        user = User.objects.get(username=self.context['request'].user)
        validated_data['user'] = user
        collection = Collection.objects.create(**validated_data)

        movies_to_create = []

        for movie_data in movies_data:
            genres_data = movie_data.pop('genres')
            genres_to_add = []

            for genre_name in genres_data:
                genre, created = Genre.objects.get_or_create(name=genre_name)

                genres_to_add.append(genre)

            movie = Movie.objects.create(**movie_data)
            movie.genres.set(genres_to_add)

            movies_to_create.append(movie)

        collection.movies.set(movies_to_create)
        return collection



class CollectionUpdateSerializer(serializers.ModelSerializer):
    movies = serializers.ListField(child=serializers.UUIDField(), required=False)
    
    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']

    def validate_title(self, value):
        user = self.context['request'].user
        existing_collections = Collection.objects.filter(user=user, title=value).exclude(pk=self.instance.pk)
        if existing_collections.exists():
            raise serializers.ValidationError("Collection with this name already exists for the user.")
        return value


    def update(self, instance, validated_data):
        # Update the collection fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        # Clear existing movies and add updated movies
        updated_movies = validated_data.get('movies', [])
        instance.movies.clear()
        for movie_uuid in updated_movies:
            movie = Movie.objects.filter(uuid=movie_uuid).first()
            if movie:
                instance.movies.add(movie)

        instance.save()
        return instance



class CollectionListSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer() 

    class Meta:
        model = Collection
        fields = ('title', 'collection_ting', 'description','user')

