from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self): 
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'
