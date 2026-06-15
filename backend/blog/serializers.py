from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created_at', 'updated_at')
        read_only_fields = ('id', 'post', 'author', 'created_at', 'updated_at')


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'slug', 'excerpt', 'image',
            'author', 'created_at', 'updated_at', 'comments_count',
        )
        read_only_fields = fields

    def get_excerpt(self, obj):
        return (obj.body[:220] + '…') if len(obj.body) > 220 else obj.body


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'slug', 'body', 'image',
            'author', 'created_at', 'updated_at', 'comments',
        )
        read_only_fields = ('id', 'slug', 'author', 'created_at', 'updated_at', 'comments')


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'image')
        read_only_fields = ('id',)
