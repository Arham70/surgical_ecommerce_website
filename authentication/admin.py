# myapp/admin.py
from django.contrib import admin
from .models import CustomUser, RequestProductForm

admin.site.register(CustomUser)
admin.site.register(RequestProductForm)

