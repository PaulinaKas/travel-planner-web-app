from django.db import models
from django.urls import reverse

# class TravelPlan(models.Model):
#     text = models.TextField()


class List(models.Model):

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class City(models.Model):
    name = models.CharField(max_length=25)
    list = models.ForeignKey(List, default=None, on_delete=models.PROTECT)
