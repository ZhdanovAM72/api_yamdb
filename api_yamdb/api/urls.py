from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (CommentViewSet,
                       ReviewViewSet,
                       UserViewSet,
                       ApiUserSignup,
                       GetApiToken)


app_name = 'api'

router = SimpleRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/token/', GetApiToken.as_view(), name='get_token'),
    path('v1/auth/signup/', ApiUserSignup.as_view(), name='signup'),
    path('v1/', include(router.urls)),
]
