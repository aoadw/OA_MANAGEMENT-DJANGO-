from . import views
from django.urls import path

app_name = 'image'

urlpatterns = [
    path('upload/', views.UploadImageView.as_view(), name='upload'),
]