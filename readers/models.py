from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    UserProfile = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    verified = models.BooleanField(verbose_name=('verified'), default=False)
    birthday=models.DateField(auto_now=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, null=True, blank=True)
    pfp = models.ImageField(null=True, blank=True, upload_to="./images/profiles")
    insta = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    tiktok = models.CharField(max_length=255, null=True, blank=True)
    youtube = models.CharField(max_length=255, null=True, blank=True)
    followers = models.ManyToManyField(User, related_name="following",blank=True)


    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('status')
        
def user_did_save(sender, instance, created, *args, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    
    if created:
        UserProfile.objects.get_or_create(user=instance)
post_save.connect(user_did_save, sender=User)