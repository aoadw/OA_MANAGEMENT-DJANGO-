from django.urls import path
from .views import LoginView,UpdatePwdView

app_name = 'oaauther'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('updatepwd/',UpdatePwdView.as_view(), name='updatepwd'),
]