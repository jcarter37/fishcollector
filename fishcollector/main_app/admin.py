from django.contrib import admin

# Register your models here.
from .models import Fish, Feeding, Lure

# Register your models here
admin.site.register(Fish)
admin.site.register(Feeding)
admin.site.register(Lure)