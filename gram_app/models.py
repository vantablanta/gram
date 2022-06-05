from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='profile/', default='profile/default.png')
    bio = models.CharField(max_length=300)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return self.name

class Image(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField( upload_to='photos/', height_field=None, width_field=None, max_length=100)
    image_name = models.CharField(max_length=200)
    image_caption = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, )
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
            return self.image_name
    
    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created']

class Comment(models.Model):
    comment = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
            return self.comment

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

