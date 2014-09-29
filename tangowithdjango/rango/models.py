from django.db import models


class Category(models.Model):
   
    name = models.CharField(max_length = 128, unique=True)

    def __unicode__(self):
        return self.name

class page(models.Model):

    category = model.ForiegnKey(Catogory)
    title = models.CharField(max_length = 128)
    url = models.UrlField()
    views = models.IntegerField(default=0)
  
    def __unicode__(self):
         return self.title
