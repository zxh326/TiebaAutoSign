from django.db import models
from django.contrib.auth.models import User,UserManager
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bduss = models.CharField(max_length=255,blank=True,null=True)
    level = models.IntegerField(blank=True,default=1)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

post_save.connect(create_user_profile, sender=User)