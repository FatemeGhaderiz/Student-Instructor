from django.db import models
from django.conf import settings 
from django.utils.translation import gettext_lazy as _

class Course(models.Model):

    slug = models.SlugField(_('slug'), max_length=100 , unique = True)
    title = models.CharField(_('title'),max_length=255)
    category = models.CharField(_('category'),max_length=255)
    is_public = models.BooleanField(_('is public'))
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_taught',verbose_name=_('instructor'))


    def __str__(self):
        return self.title
    


    
class Content(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents', verbose_name=_('course'))
    title = models.CharField(_('title'),max_length=255)
    file = models.FileField(_('file'), upload_to='contents/', blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Exercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exercises', verbose_name=_('course'))
    title = models.CharField(_('title'),max_length=255)
    text = models.TextField( blank=True, null=True)
    file = models.FileField(_('file'), upload_to='contents/', blank=True, null=True)
    deadline = models.DateField()

    def __str__(self):
        return self.title

class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements', verbose_name=_('course'))
    title = models.CharField(_('title'),max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title