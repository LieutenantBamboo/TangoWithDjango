from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    max_length = 128
    name = models.CharField(max_length=max_length, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if self.views < 0:
            self.views = 0
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    max_length = 128
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class UserProfile(models.Model):
    # Required Line - links class to model instance
    user = models.OneToOneField(User)

    # Additonal Attributes:
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # __unicode__() override
    def __str__(self):
        return self.user.username

    # Defined for compatability's sake
    def __unicode__(self):
        return self.user.username
