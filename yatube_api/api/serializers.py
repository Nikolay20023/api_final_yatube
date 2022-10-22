from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group, Follow, User
from rest_framework.validators import UniqueTogetherValidator


class PostSerializer(serializers.ModelSerializer):
    """Реализуем сериализацию для модели Post, всё по стандарту."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """Модель и поля."""

        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Реализуем сериализацию для модели Comment, всё по стандарту,."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        """Модель и поля."""

        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """Реализуем сериализацию для модели Group, всё по стандарту,."""

    class Meta:
        """Модель и поля."""

        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Реализуем сериализацию для модели Group, queryset еще."""

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=(
            serializers.CurrentUserDefault()
        )
    )

    class Meta:
        """Модель и поля и еще валидация на уинкальные поля."""

        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate(self, data):
        """Проверяем чтобы пользователь сам на себя не подписался."""
        if data['following'] == self.context.get('request').user:
            raise serializers.ValidationError('Подписка самого на себя')
        return data
