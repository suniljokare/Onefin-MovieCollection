from django.conf import settings
import requests
from app.models import User, Collection, RequestCount
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from app.serializers import (
    CollectionSerializer, 
    CollectionListSerializer, 
    CreateCollectionSerializer, 
    UserRegistrationSerializer, 
    CollectionUpdateSerializer )

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from retrying import retry

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserRegistrationSerializer  
    permission_classes = [AllowAny]  

    # @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


    def login(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                return Response({"access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
                

class GetMoviesFromThirdPartyAPI(APIView):
    permission_classes = [IsAuthenticated]  
    
    @retry(
        stop_max_attempt_number=3,  # Maximum number of retry attempts
        wait_fixed=2000  # Wait for 2 seconds between retries
    )
    def get(self, request):
        try:
            username = getattr(settings, "USERNAME")
            password = getattr(settings, "PASSWORD")
            api_url = "https://demo.credy.in/api/v1/maya/movies/"

            response = requests.get(api_url, auth=(username, password), verify=False)
            if response.status_code == 200:
                data = response.json()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Failed to fetch data from the API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except requests.exceptions.RequestException as e:
            raise e

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionViewSet(viewsets.ModelViewSet):
    # queryset = Collection.objects.filter(is_deleted=False) 
    permission_classes = [IsAuthenticated]  

    serializer_classes = {
        "create": CreateCollectionSerializer,
        "retrieve": CollectionSerializer,
        "update":CollectionUpdateSerializer,
        "user_collections": CollectionListSerializer
    }
 
    def get_queryset(self, user):
        return Collection.active_collections.filter(user=user)
    
    # def get_object(self, **kwargs):
    #     return Collection.objects.get(**kwargs)
    
    def get_object(self, **kwargs):
        return Collection.active_collections.get(**kwargs)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

  

    def get_favorite_genres(self, collections):
        genre_count = {}

        # Iterate through all movies in the user's collections
        for collection in collections:
            for movie in collection.movies.all():
                genres = movie.genres.all()  # Use .all() to get all genres for the movie
                for genre in genres:
                    genre_count[genre.name] = genre_count.get(genre.name, 0) + 1

        sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)

        # Get the top 3 favorite genres
        favorite_genres = ', '.join([genre for genre, count in sorted_genres[:3]])

        return favorite_genres
    

    def user_collections(self, request):
        try:
            user = self.request.user
            if user is None:
                return Response({"error": "User not provided"}, status=status.HTTP_400_BAD_REQUEST)

            collections = Collection.objects.filter(user=user)
            
            serializer = CollectionListSerializer(collections, many=True)
            favorite_genres = self.get_favorite_genres(collections)

            response_data = {
                "is_success": True,
                "data": {
                    "collections": serializer.data,
                    "favourite_genres": favorite_genres 
                }
            }

            return Response(response_data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def retrieve(self, request, collection_uuid=None):
        try:
            instance = Collection.objects.get(collection_ting=collection_uuid)
            serializer = self.get_serializer_class()(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def create(self, request):
        try:
            serializer = self.get_serializer_class()(data=request.data, context={"request": request})

            if serializer.is_valid():
                collection = serializer.save()
                response_data = {"collection_uuid": str(collection.collection_ting)}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, collection_uuid=None):
        try:
            instance = self.get_object(collection_ting=collection_uuid)
            serializer = self.get_serializer_class()(instance, data=request.data, context={"request": request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Collection updated successfully"} ,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def delete_collection(self, request, collection_uuid=None):
        try:
            # collection = self.get_object()
            instance = self.get_object(collection_ting=collection_uuid)
            instance.soft_delete()

            return Response({"message": "Collection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                

class RequestCountView(APIView):
    def get(self, request):
        request_count = RequestCount.objects.first()
        response_data = {"requests": request_count.count if request_count else 0}
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        request_count = RequestCount.objects.first()
        if request_count:
            request_count.count = 0
            request_count.save()
        response_data = {"message": "Request count reset successfully"}
        return Response(response_data, status=status.HTTP_200_OK)
