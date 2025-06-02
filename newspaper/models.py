from django.db import models

# Create your models here.


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampModel): 
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True, blank=True)  
    description = models.TextField(null=True, blank=True) 
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name = "category"  
        verbose_name_plural = "categories"


class Tag(TimeStampModel):  
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(TimeStampModel):  
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),  
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_image/%Y/%m/%d", blank=False)  
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    views_count = models.PositiveBigIntegerField(default=0) 
    published_at = models.DateTimeField(null=True, blank=True)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    tag = models.ManyToManyField(Tag) 
    def __str__(self):
        return self.title


class Advertisement(TimeStampModel):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="advertisements/%Y/%m/%d", blank = False )

    def __str__(self):
        return self.title