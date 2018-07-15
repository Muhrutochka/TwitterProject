import re

from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

# class TweetManager(models.Manager):
#     def retweet(self, user, parent_obj):
#         if parent_obj.parent:
#             og_parent = parent_obj.parent
#         else:
#             og_parent = parent_obj
#
#         obj = self.model(
#             parent = og_parent,
#             userid = user,
#             text = parent_obj.content,
#         )
#         obj.save()
#         return obj

class Messages(models.Model):
    text = models.CharField(max_length=260)
    dateadd = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.PROTECT)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    reply = models.BooleanField(verbose_name='Is a reply?', default=False)


    # objects = TweetManager()


    # def __str__(self):
    #     return str(self.content)


    def get_absolute_url(self):
        return reverse("tweet:detail", kwargs={"pk": self.pk})


    class Meta:
        ordering = ['-dateadd']


    def get_parent(self):
        the_parent = self
        if self.parent:
            the_parent = self.parent
        return the_parent


    def get_children(self):
        parent = self.get_parent()
        qs = Messages.objects.filter(parent=parent)
        qs_parent = Messages.objects.filter(pk=parent.pk)
        return (qs | qs_parent)
