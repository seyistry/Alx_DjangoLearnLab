from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'book', BookViewSet)


urlpatterns = [
    path('api/', BookList.as_view(), name='book_list'),
    path('api/', include(router.urls)),
]
