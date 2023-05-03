from django.urls import path
from accounts.views import logout_user, login_user, signup, profile, set_address, activation_user, welcome_message, \
    follow

app_name = "accounts"
urlpatterns = [
    path('profile/<str:username>/', profile, name='profile'),
    path('follow/<str:username>/', follow, name='follow'),
    # path('set-address', set_address, name='set-address'),
    path('singup/', signup, name='singup'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('user-validate/<str:uidb64>/<str:token>/', activation_user, name='user-activation-link'),
    path('welcome/', welcome_message, name='welcome-message')

]
