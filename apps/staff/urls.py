from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('departments/', views.DepartmentList.as_view(), name='department'),
]