from django.contrib import admin

# Register your models here.
from .models import Payment, Amount

# Register your models here.
admin.site.register(Payment)
admin.site.register(Amount)
