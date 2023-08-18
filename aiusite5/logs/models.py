from django.db import models
import datetime

# Create your models here.
#
#class Topic(models.Model):
#	text = models.CharField(max_length=200)
#	date_added = models.DateTimeField(auto_now_add=True)
# 
#	def __str__(self):
#		return self.text
 
#class Entry(models.Model):
#	topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
#	text = models.TextField()
#	date_added = models.DateTimeField(auto_now_add=True)
# 
#	class Meta:
#		verbose_name_plural = 'entries'	
# 
#	def __str__(self):
#		return self.text[:50] + "..."
class Post(models.Model):
    image = models.FileField(upload_to='images/')
    title = models.CharField(default="", max_length=64)
    description = models.CharField(default="", max_length=512)
    date = models.DateField(default=datetime.date.today)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
