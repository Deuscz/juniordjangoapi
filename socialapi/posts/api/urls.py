from django.urls import path
from posts.api.views import *

urlpatterns = [
    path('post/<str:slug>/', PostView.as_view(), name="detail"),
    path('post/<str:slug>/like/', PostLikeView.as_view(), name="like"),
    path('all/', PostListView.as_view(), name="list"),
    path('create/', PostCreate.as_view(), name="create"),

]
