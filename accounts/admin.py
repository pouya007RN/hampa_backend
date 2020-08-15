from django.contrib import admin
from accounts.models import Account, Profile, Address
# Register your models here.

admin.site.register(Account)
admin.site.register(Profile)
admin.site.register(Address)
