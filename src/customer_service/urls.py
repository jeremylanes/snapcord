from django.urls import path

from customer_service.views import about, message, thanks

app_name = "customer_service"
urlpatterns = [
    path('about/', about, name='about'),
    path('message/', message, name='message'),
    path('thanks/', thanks, name='thanks')
]
