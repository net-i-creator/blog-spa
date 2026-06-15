from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostWriteSerializer,
    CommentSerializer,
)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        author = getattr(obj, 'author', None)
        return bool(author and author == request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'body']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ('list',):
            return PostListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return PostWriteSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        write = PostWriteSerializer(data=request.data)
        write.is_valid(raise_exception=True)
        post = write.save(author=request.user)
        return Response(
            PostDetailSerializer(post, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        write = PostWriteSerializer(post, data=request.data, partial=True)
        write.is_valid(raise_exception=True)
        post = write.save()
        return Response(PostDetailSerializer(post, context={'request': request}).data)


class CommentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    parser_classes = [JSONParser]

    def list(self, request, post_slug=None):
        post = get_object_or_404(Post, slug=post_slug)
        qs = post.comments.select_related('author').all()
        return Response(CommentSerializer(qs, many=True, context={'request': request}).data)

    def create(self, request, post_slug=None):
        post = get_object_or_404(Post, slug=post_slug)
        ser = CommentSerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save(post=post, author=request.user)
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        return Response(CommentSerializer(comment, context={'request': request}).data)

    def partial_update(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        ser = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    def destroy(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
