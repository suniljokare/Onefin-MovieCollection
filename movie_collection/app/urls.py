from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CollectionViewSet, RequestCountView,GetMoviesFromThirdPartyAPI, UserViewSet
# from django.urls import reverse

router = DefaultRouter()
# login_url = reverse('login')
# router.register(r'collection', CollectionViewSet),

urlpatterns = router.urls

urlpatterns += [
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('movies/', GetMoviesFromThirdPartyAPI.as_view(), name='get-movies'),
    path('collections/', CollectionViewSet.as_view({'get': 'user_collections', 'post': 'create'}), name='collection-list'),
    path('collections/<uuid:collection_uuid>/', CollectionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete_collection'}), name='collection-detail'),
    path('request-count/', RequestCountView.as_view(), name='request-count'),
    path('request-count/reset/', RequestCountView.as_view(), name='reset-request-count'),

]