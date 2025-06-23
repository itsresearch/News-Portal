from django.contrib.auth.models import User, Group
from rest_framework import  permissions, viewsets # type: ignore
from api.serializers import PostSerializer, UserSerializer, GroupSerializer, TagSerializer, CategorySerializer
from newspaper.models import Post, Tag, Category
from rest_framework.generics import ListAPIView # type: ignore
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):
    queryset=Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [permissions.AllowAny()]
        
        return super().get_permissions()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [permissions.AllowAny()]
        
        return super().get_permissions()

class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all().order_by('-published_at')
    serializer_class=PostSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ['list','retrieve']:
            queryset= queryset.filter(status="active", published_at__isnull=False)

        return queryset
    
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [permissions.AllowAny()]
        
        return super().get_permissions()
    

class PostListByCategory(ListAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permissions_classes=[permissions.AllowAny]

    def get_querset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(
            satus="active",
            published_at__isnull=False,
            category=self.kwargs["category_id"]
        )
        return queryset
