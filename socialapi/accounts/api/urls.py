from django.urls import path
from accounts.api.views import RegistrationView, UsersList, UserDetail
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('all-accounts/', UsersList.as_view(), name='user_list'),
    path('all-accounts/<str:email>/', UserDetail.as_view(), name='user_detail')
]