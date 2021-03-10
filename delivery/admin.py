from django.contrib import admin
from .models import UserProfile, ProductTable, DelDetails
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(ProductTable)
admin.site.register(DelDetails)

