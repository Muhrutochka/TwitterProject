from django.db import models

class Messages(models.Model):
    text = models.CharField(max_length=260)
    dateadd = models.DateTimeField(auto_now_add=True)
    userid = models.IntegerField()

