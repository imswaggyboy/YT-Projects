from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
from taggit.managers import TaggableManager

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                    .filter(status=Post.Status.PUBLISHED)



class Post(models.Model):

    #adding status field
    class Status(models.TextChoices):
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField( max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author  = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    liked_by = models.ManyToManyField(User, related_name='liked_post')
    image = models.ImageField(upload_to='blog_pics',null=True,blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    objects = models.Manager() #the default manager
    published = PublishedManager()
    tags = TaggableManager()

    #count like
    def number_of_like(self):
        return self.liked_by.count()
    


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

        # if self.image:
        #     img = Image.open(self.image )
        #     # print(img.height,img.width)

        #     if img.height > 500 or img.width > 950:
        #         output_size = (950,500) 
        #         img.thumbnail(output_size)
        #         img.save(self.image.path)


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year,
                                                  self.publish.month,
                                                  self.publish.day,
                                                  self.slug,
                                                  self.id])

class PostComments(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_likes = models.ManyToManyField(User,related_name='comment_likes')
    comment= models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


    def number_of_likes_comment(self):
        return self.comment_likes.count()
    class Meta:
        ordering = ['created']


    def __str__(self):
        return f"{self.name} commented on {self.post}"
