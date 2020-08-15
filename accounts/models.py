from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Account(AbstractUser):
    phone_number = models.CharField(max_length=500, blank=True, null=True, default=None)
    is_producer = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="media/", default='', null=True, blank=True)
    credit = models.IntegerField(null=True, blank=True, default=10000)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=Account)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()


class Address(models.Model):
    profile = models.ForeignKey(Profile, related_name='addresses', on_delete=models.CASCADE, null=True, blank=True)
    province = models.CharField(max_length=30, default='', null=True, blank=True)
    city = models.CharField(max_length=30, default='', null=True, blank=True)
    address = models.TextField(default='')

    def __str__(self):
        return '%s -> %s' % (self.province, self.city)
