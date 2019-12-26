from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from posts.api.serializers import PostsSerializer
from posts.models import Post
from accounts.models import Account
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly


class PostLikeView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostsSerializer
    lookup_field = 'slug'
    def post(self, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        username = self.request.user.username
        account = get_object_or_404(Account, username=username)
        if account in post.likes.all():
            post.likes.remove(account)
        else:
            post.likes.add(account)
        serialized_data = PostsSerializer(post).data
        serialized_data['likes'] = post.likes.all().count()
        serialized_data['author'] = post.author.__str__()
        return Response(serialized_data)


class PostCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostsSerializer

    def post(self, request, *args, **kwargs):
        account = get_object_or_404(Account, email=self.request.user.email)
        post = Post(author=account)
        serializer = PostsSerializer(post, data=self.request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            serialized_data['likes'] = post.likes.all().count()
            serialized_data['author'] = post.author.__str__()
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostsSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset


class PostView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = PostsSerializer
    lookup_field = 'slug'

    def get(self, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        serialized_data = PostsSerializer(post).data
        serialized_data['likes'] = post.likes.all().count()
        serialized_data['author'] = post.author.__str__()
        return Response(serialized_data)
