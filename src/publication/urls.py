from django.urls import path

from publication.views import new_post, comment, react

app_name = "publication"
urlpatterns = [
    path('new-post/', new_post, name='new_post'),
    path('comment/<int:pk>/', comment, name='comment'),
    path('react/<int:pk>/', react, name='react')

]
