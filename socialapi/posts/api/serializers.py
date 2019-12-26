from rest_framework import serializers
from posts.models import Post


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'text', 'publish_date', 'author', 'likes', 'slug']
        extra_kwargs = {
            'author': {'read_only': True},
            'likes': {'read_only': True},
            'slug': {'read_only': True},
            'publish_date': {'read_only': True},
        }
