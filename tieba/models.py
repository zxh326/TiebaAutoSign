from django.db import models
from django.contrib.auth.models import User,UserManager
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bduss = models.CharField(max_length=255,blank=True,null=True,default='null')
    level = models.IntegerField(blank=True,default=1)
    tieba_count = models.IntegerField(blank=True,null=True)
    sign_sum = models.IntegerField(blank=True,null=True)
    sign_count = models.IntegerField(blank=True,null=True)
    
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

class TiebaList(models.Model):
    fid = models.IntegerField()
    tiebaname = models.CharField(max_length=50)
    user = models.ForeignKey(User, models.DO_NOTHING)
    error_code = models.IntegerField(blank=True, null=True)
    error_msg = models.CharField(max_length=100, blank=True, null=True)
    is_sign = models.DateField(blank=True, null=True)