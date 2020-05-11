from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User)
    date_of_birth= models.DateField(blank=True,null=True)
    photo=models.ImageField(upload_to='user/%Y/%m/%d',blank=True)
    REQUIRED_FIELDS=''
    USERNAME_FIELD=""
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()



class Contact(models.Model):
    user_from = models.ForeignKey(User,related_name='rel_from_set')
    user_to = models.ForeignKey(User,related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    class Meta:
        ordering = ('-created',)     #按created倒序排序
    def __str__(self):
        return '{} follows {}'.format(self.user_from,self.user_to)

User.add_to_class('following',models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False))