from rest_framework import generics

from aiacademies_api.permissions import IsSuperUser, IsGet
from .models import Post
from .serializers import PostSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsGet | IsSuperUser]


class PostInstanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'
    permission_classes = [IsGet | IsSuperUser]
