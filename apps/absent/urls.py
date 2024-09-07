from django.urls import path
from rest_framework import routers

from apps.absent import views

app_name = 'absent'

router = routers.DefaultRouter()
router.register('absent', views.AbsentViewSet, basename='absent')

urlpatterns = [
    path('types/',views.AbsentTypesView.as_view(),name='types'),
    path('responser/',views.ResponserView.as_view(),name='responser'),
              ] + router.urls