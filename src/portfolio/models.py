from __future__ import unicode_literals


from django.db import models

class Stocks(models.Model):
	name = models.CharField(max_length=120)
	description = models.TextField()

	def __unicode__(self):
		return self.name

# Create your models here.
