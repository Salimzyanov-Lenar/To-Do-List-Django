from django.urls import path
from users.views import logout_view, UserLoginView, UserRegisterView


urlpatterns = [
    # users/
    path('signup/', UserRegisterView.as_view(), name='register_page'),
    path('login/', UserLoginView.as_view(), name='login_page'),
    path('logout/', logout_view, name='logout'),
]