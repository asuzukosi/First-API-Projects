from django.urls import path, include
from .views import home, ArticleViewSet, CarAPIView, CarDetailAPIView, PersonsAPIView, PersonDetailsAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='article')


urlpatterns = [
    path("", home, name="Home"),
    path('api/', include(router.urls)),
    path('api/cars', CarAPIView.as_view(), name='Cars'),
    path('api/cars/<int:pk>', CarDetailAPIView.as_view(), name='Car'),
    path('api/persons', PersonsAPIView.as_view(), name='Persons'),
    path('api/persons/<int:pk>', PersonDetailsAPIView.as_view(), name='Person'),

]
