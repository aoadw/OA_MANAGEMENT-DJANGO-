from rest_framework import routers
from . import views

app_name = 'inform'

router = routers.DefaultRouter()
router.register('inform', views.InformViewSet, basename='inform')

urlpatterns = [] + router.urls