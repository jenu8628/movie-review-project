from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup),
    path('api-token-auth/', obtain_jwt_token),
    path('identify_user_superuser/',views.identify_user_superuser),
    path('get_username/',views.get_username),
]