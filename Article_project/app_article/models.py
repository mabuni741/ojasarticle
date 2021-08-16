import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Token(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4(), editable=False)
    is_expired = models.BooleanField(default=False)


class ArticleModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=20, choices=(
        ('arch', 'Architecture'),
        ('news','News'),
        ('heal', 'Health'),
        ('politics','Politics'),
        ('sports','Sports'),
        ('beauty','Beautytips'),
        ('other','Others')
        
    ))
    title = models.CharField(max_length=500)
    data = models.TextField(max_length=1000,blank=True,null=True)
    created_on = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    
    def publish(self):
        self.published_date = timezone.now()
        self.save()



    def __str__(self):
        return self.title


class ContactUs(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message = models.TextField(max_length=1000,blank=True,null=True)
    
    def __str__(self):
        return self.name



class comment(models.Model):
    post=models.ForeignKey(ArticleModel,related_name='comments',on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    body=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering=['date_added']   

      