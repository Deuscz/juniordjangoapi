from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts API
    path('api/accounts/', include('accounts.api.urls'), name='accounts'),

    # Posts API
    path('api/posts/', include('posts.api.urls'), name='posts'),
    path("api-auth/", include("rest_framework.urls")),

    # Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
