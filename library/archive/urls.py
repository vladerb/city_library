from django.urls import path
from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.PostListView.as_view(), name='books-list'),
]