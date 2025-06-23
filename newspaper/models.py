from django.db import models

class TimeStampModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract=True # Don't create table in DB

    
class Category(TimeStampModel):
    name=models.CharField(max_length=100)
    icon=models.CharField(max_length=100,null=True, blank=True)
    description=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering=['name'] #Category.objects.all
        verbose_name="categories"
        verbose_name_plural="Categories"

class Tag(TimeStampModel):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Post(TimeStampModel):
    STATUS_CHOICES=[
        ("active","Active"),
        ('in_active', 'Inactive')
    ]
    title=models.CharField(max_length=200)
    content=models.TextField()
    featured_image=models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False)
    author=models.ForeignKey("auth.User",on_delete=models.CASCADE)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES,default="active")
    views_count=models.PositiveBigIntegerField(default=0)
    published_at=models.DateTimeField(null=True, blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Advertisement(TimeStampModel):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="advertisements/%Y/%m/%d", blank=False)

    def __str__(self):
        return self.title
    
class UserProfile(TimeStampModel):
    user=models.OneToOneField("auth.User", on_delete=models.CASCADE)
    image=models.ImageField(upload_to="user_image/%Y/%m/%d", blank=False)
    address=models.CharField(max_length=200)
    biography=models.TextField()

    def __str__(self):
        return self.user.username

# post - comment
# 1 post can have M comments => M
# 1 comment can have 1 post => 1

# comment - user
# 1 user can add M comments => M
# 1 comment can have 1 user => 1

class Comment(TimeStampModel):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,)
    user=models.ForeignKey("auth.User", on_delete=models.CASCADE)
    content=models.TextField()
    
    def __str__(self):
        return f"{self.content[:50]} | {self.user.username}"

class Contact(TimeStampModel):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=200)
    message=models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering=['created_at']

class NewsLetter(TimeStampModel):
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.email