from django.urls import path
from .views import post_list_view
from . import views

app_name = "posts"

urlpatterns = [
    path("", post_list_view, name="list"),
    path("uploadpost/", views.upload , name='upload_post'),
    path("user/<str:pathUsername>/", views.filter_username, name='filter_by_username'),
    path("deletepost/<int:id>", views.delete, name='delete'),
    path("updatepost/<int:id>", views.update, name='update'),
    path("updatepost/<int:id>/confirm", views.updateConfirm, name='updateConfirm')

]
