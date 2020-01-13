from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
# Create your models here.
class Profile(models.Model):
    name=models.CharField(max_length=30)
    Bio= models.TextField()
    profile_image=models.ImageField(upload_to = 'profiles/',blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    follow=models.ManyToManyField(User,related_name='who_following',blank=True)
    def __str__(self):
        return self.name


    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
    def save_profile(self):
        self.save()
    def delete_profile(self):
        self.delete()
    @classmethod
    def search(cls,search_term):
        profiles=cls.objects.filter(name__icontains=search_term)
        return profiles
    @classmethod
    def get_profile(cls):
        profile=Profile.objects.all()
        return profile
    def total_following(self):
        return self.follow.count()
class Image(models.Model):
    name=models.CharField(max_length=20)
    image_caption=models.CharField(max_length=1000,blank=True)
    image_path=models.ImageField(upload_to='images/',blank=True)
    profile=models.ForeignKey(Profile,null=True)
    likes=models.ManyToManyField(User,related_name='likes' ,blank=True)
    def save_image(self):
        self.save()
    def delete_image(self):
        self.delete()
    @classmethod
    def get_id(cls):
        prof=Image.objects.all()
        return prof
    @classmethod
    def get_image(cls):
        images=Profile.objects.all()
        return images
    def total_likes(self):
        return self.likes.count()
class Comment (models.Model):
    comment=models.CharField(max_length=50)
    image=models.ForeignKey(Image,null=True)
    user=models.ForeignKey(User,null=True)

#Add the following field to User dynamically
