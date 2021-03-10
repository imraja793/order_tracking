from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone

from django.db.models.signals import pre_save
from django.dispatch import receiver


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_delivery_guy = models.BooleanField(default=True)
    lat_long = models.CharField(max_length=50)

    class Meta:
        ordering = ['id']

    # def __str__(self):
    #     return self


class ProductTable(models.Model):
    item = models.CharField(max_length=100, null=True, blank=True)
    unique_id = models.CharField(max_length=20)

    def __str__(self):
        return self.item


@receiver(pre_save, sender=ProductTable)
def my_callback(sender, instance, *args, **kwargs):
    instance.unique_id = random.randint(1, 90000000)


class DelDetails(models.Model):

    unique_delivery_id = models.CharField(max_length=200)
    itemdetails = models.ForeignKey(ProductTable, on_delete=models.CASCADE, null=True, blank=True)
    lat_long_initial = models.CharField(max_length=50, null=True, blank=True)
    destination_lat_long = models.CharField(max_length=50, null=True, blank=True)
    time_spent = models.CharField(max_length=20, null=True, blank=True)
    delivery_delayed = models.BooleanField(default=False)
    delivery_details = models.CharField(max_length=200, null=True, blank=True)
    assigned_delivery_guy = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    previous_address = models.CharField(max_length=50, null=True, blank=True)
    delivery_number = models.IntegerField(default=1)
    distance_travelled = models.CharField(max_length=20, default=0)
    delivery_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.delivery_details



