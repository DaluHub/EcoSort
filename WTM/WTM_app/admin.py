from django.contrib import admin
from .models import CustomUser, Company, WastePickupRequest, Reward, Transaction

admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(WastePickupRequest)
admin.site.register(Reward)
admin.site.register(Transaction)
# Register your models here.
