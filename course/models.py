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
    

