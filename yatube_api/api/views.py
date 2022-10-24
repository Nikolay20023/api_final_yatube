from .serializers import (
    GroupSerializer,
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
)

from rest_framework import viewsets
from posts.models import Post, Group
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .permission import IsOwnerOrReadOnly
from rest_framework.pagination import (
    LimitOffsetPagination,
)
from rest_framework import filters


class PostViewSet(viewsets.ModelViewSet):
    """Viewset для постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """метод для создания , переопределение постов."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset для comment."""

    serializer_class = CommentSerializer
    permission_classes = (permissions.AllowAny, IsOwnerOrReadOnly)

    def get_queryset(self):
        """Делаем запрос к базе данных через встроенный метод."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments

    def perform_create(self, serializer):
        """Создаём комментариий с помощью встроенного метода."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset только для чтения то есть для Get запросов."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class FollowViewSet(viewsets.ModelViewSet):
    """Viewset для модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, )
    filter_fields = ('user', 'following')
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        """Выполним запрос к БД."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Создаём подписку,только для авторизованных клиентов."""
        serializer.save(user=self.request.user)
