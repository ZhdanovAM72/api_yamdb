from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import UserViewSet, ApiUserSignup, GetApiToken


app_name = 'api'

router = SimpleRouter()
router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/auth/token/', GetApiToken.as_view(), name='get_token'),
    path('v1/auth/signup/', ApiUserSignup.as_view(), name='signup'),
    path('v1/', include(router.urls)),
]
