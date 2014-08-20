from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
import datetime


GENDER_CHOICES = (
    ('M', _('Male')),
    ('F', _('Female')),
)


YEAR_CHOICES = []
for r in reversed(range((datetime.datetime.now().year-80), (datetime.datetime.now().year-12))):
    YEAR_CHOICES.append((r,r))


class Instrument(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
    
    def __unicode__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.name
    

class Region(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name
    

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    bio = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    region = models.ForeignKey(Region, blank=True, null=True)
    instruments = models.ManyToManyField(Instrument, blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('user', args=(self.username,))

    @staticmethod
    def get_queryset(params):
        instruments = params.get('instruments')
        qset = Q()
        if instruments:
            qset &= Q(instruments__in = instruments)
        return qset
