from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.urlresolvers import reverse
# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(User,related_name='images_created')    #一对多关系,一个用户多张图片
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y%m%d')
    description =models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,db_index=True)
    user_like = models.ManyToManyField(User,related_name='images_liked',blank=True)     #喜欢这张图片的用户
    total_likes = models.PositiveIntegerField(db_index=True,
                                              default=0)
    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):  #重写save自动生成slug
        if not self.slug:
            self.slug = slugify(self.title)     #没有提供slug时自动生成
            super(Image,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id,self.slug]) #不能乱加空格