from django.contrib import admin
from .models import veterinarian
from .models import feedback
# Register your models here.

admin.site.register(veterinarian)
admin.site.register(feedback)
