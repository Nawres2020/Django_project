from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from django.contrib.auth.models import Group





#custimize the groupuser in the default django group
class CustomGroupUser(Group):
    description = models.TextField(blank=True)
    date_of_creation= models.DateField(blank=True, null=True)



#custmize the userProfile , extend from the user's model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username
   
    

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

