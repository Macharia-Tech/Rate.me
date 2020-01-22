from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


#Add the following field to User dynamically
class Profile(models.Model):
    '''
    Class that contains User Profile details
    '''
    profile_photo=models.ImageField(upload_to='images/',blank=True)
    bio=models.CharField(max_length=100)
    contact=models.CharField(max_length=25)
    editor = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.editor.username} Profile'
    @receiver(post_save, sender=User)
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(editor=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        '''
        Setting up self 
        '''
        return self.bio

    @classmethod
    def get_profile(cls):
        '''
        Method to retrieve the profile details
        '''
        profile=cls.objects.all()
        return profile

    def save_profile(self):
        '''
        Method to save the created profile
        '''
        self.save()

    def delete_profile(self):
        '''
        Method to delete the profile
        '''
        self.delete()

    @classmethod
    def single_profile(cls,user_id):
        '''
        function gets a single profile posted by id
        '''
        profile=cls.objects.filter(id=user_id)
        return profile

    @classmethod
    def get_profilepic_id(cls,imageId):
        '''
        function that gets a profilepic id    
        '''
        image_id=cls.objects.filter(id=imageId)
        return image_id

class Project(models.Model):
    title=models.CharField(max_length=30)
    image=models.ImageField(upload_to='images/',blank=True)
    description=models.CharField(max_length=255)
    link=models.URLField( max_length=128, db_index=True,unique=True,blank=True)
    editor = models.ForeignKey(User,on_delete=models.CASCADE)
  

    def __str__(self):
        '''
        Setting up self
        '''
        return self.title

    def save_project(self):
        '''
        Method for saving the project
        '''
        self.save()

    def delete_project(self):
        '''
        Method for deleting the project
        '''
        self.delete()
    
    @classmethod
    def get_projects(cls):
        '''
        Method for retrieving all images
        '''
        project=cls.objects.all()
        return project

    @classmethod
    def user_projects(cls,user_id):
        '''
        function gets projects posted by id
        '''
        project_posted=cls.objects.filter(editor=user_id)
        return project_posted    

    @classmethod
    def search_by_title(cls,tag):
        '''
        Method for searching for a project using the title
        '''

        search_result=cls.objects.filter(title__icontains=tag)
        return search_result

    @classmethod
    def single_project(cls,project_id):
        '''
        function gets a single project posted by id
        '''
        project_posted=cls.objects.get(id=project_id)
        return project_posted

    @classmethod
    def get_image_id(cls,imageId):
        '''
        function that gets an image id    
        '''
        image_id=cls.objects.filter(id=imageId)
        return image_id

class Rating(models.Model):
    editor=models.ForeignKey(User,on_delete=models.CASCADE)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    design=models.IntegerField()
    usability=models.IntegerField()
    content=models.IntegerField()


    def __str__(self):
        '''
        Setting up self
        '''
        return self.design

    @classmethod
    def get_rating_byproject_id(cls,project_id):
        rating=cls.objects.filter(project=project_id)
        return rating