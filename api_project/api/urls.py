from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import IsAuthenticated, IsAdminUser

router = DefaultRouter()
router.register(r'book', BookViewSet)


urlpatterns = [
    path('api/', BookList.as_view(), name='book_list'),
    path('api/', include(router.urls)),
	path('api/token', obtain_auth_token, name='api_token_auth')
]
