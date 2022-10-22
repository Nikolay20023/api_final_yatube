from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet
)

router = SimpleRouter()

router.register(r'posts', PostViewSet, basename="posts")
router.register(r'groups', GroupViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path(r'v1/', include(router.urls)),
    path(r'v1/', include('djoser.urls')),
    path(r'v1/', include('djoser.urls.jwt')),
]
